from fastapi import Depends, HTTPException, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from ..models.database import get_db
from app.models.tables import Menu, Category
from app.schemas.user import TokenData
from app.schemas.menu import Menus, MenuCreate, MenuUpdate
from ..utils import auth, constants

router = APIRouter(prefix="/menus", tags=["Menu"])

def check_valid_category(id: int, db: Session):
    category = db.query(Category).filter(
        Category.id == id,
        Category.status == True
    ).first()
    
    return category is not None


@router.get("/", response_model=List[Menus])
def get_menus(db: Session = Depends(get_db), 
              userData: TokenData = Depends(auth.get_current_user),
              page_index: int = Query(1, ge=1),
              page_size: int = Query(10, le=100)):
    query = db.query(Menu)
    
    if userData.role != constants.ROLE_ADMIN:
        query = query.filter(Menu.status == True)
        
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No categories found!"
        )
    
    total_size = query.count()
    total_page = (total_size + page_size - 1) // page_size

    if page_index > total_page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page index out of range!"
        )

    page_skip = (page_index - 1) * page_size
    menus = query.offset(page_skip).limit(page_size).all()
    return menus

@router.get("/{id}", response_model=Menus)
def get_menu_by_id(id: int,
                   db: Session= Depends(get_db),
                   userData: TokenData = Depends(auth.get_current_user)):
    menu = db.query(Menu).filter(Menu.id == id)
    
    if userData.role != constants.ROLE_ADMIN:
        menu = menu.filter(Menu.status == True)
        
    menu = menu.first()
    
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no menu with id {id}!" 
        )
    
    return menu

@router.post("/", response_model=List[Menus], status_code=status.HTTP_201_CREATED)
def create_menus(menus: List[MenuCreate],
                 db: Session = Depends(get_db),
                 userData: TokenData = Depends(auth.get_current_user)):
    if userData.role != constants.ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized" 
        )
        
    for menu in menus:
        if not check_valid_category(menu.category_id, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid category id: {menu.category_id}"
            )
    
    db_menus = [Menu(**menu.dict()) for menu in menus]
    db.add_all(db_menus)
    db.commit()
    return db_menus

@router.patch("/", status_code=status.HTTP_202_ACCEPTED)
def update_menus(menus: List[MenuUpdate],
                  db: Session = Depends(get_db),
                  userData: TokenData = Depends(auth.get_current_user)):    
    if userData.role != constants.ROLE_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized")

    for menu in menus:
        db_menu = db.query(Menu).filter(Menu.id == menu.id).first()
        
        if not db_menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Menu not found")
        
        [setattr(db_menu, key, value) for key, value in menu.dict(exclude_unset=True).items()]

        db_menu.update_at = func.now()
                
    db.commit()
    return {"detail": "Menus updated successfully"}

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_menus(id: List[int],
                 db : Session = Depends(get_db),
                 userData: TokenData = Depends(auth.get_current_user)):
    if userData.role != constants.ROLE_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized")
    
    menus = db.query(Menu).filter(Menu.id.in_(id)).all()
    if not menus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No menus found with the provided IDs")

    for menu in menus:
        if menu.status == True:
            menu.status = False
            menu.update_at = func.now()
        
    db.commit()
    
    return {"detail": "Menus deleted"}