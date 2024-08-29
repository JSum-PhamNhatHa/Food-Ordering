from fastapi import Depends, HTTPException, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from ..models.database import get_db
from app.models.tables import Category
from app.schemas.user import TokenData
from app.schemas.category import Categories, CategoryCreate, CategoryUpdate
from ..utils import auth, constants

router = APIRouter(prefix="/categories", tags=["Category"])

@router.get("/", response_model=List[Categories])
def get_categories(db: Session = Depends(get_db), 
                   userData: TokenData = Depends(auth.get_current_user),
                   page_index: int = Query(1, ge=1),
                   page_size: int = Query(10, le=100)):
    query = db.query(Category)
    
    if userData.role != constants.ROLE_ADMIN:
        query = query.filter(Category.status == True)
        
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
    categories = query.offset(page_skip).limit(page_size).all()
    return categories

@router.get("/{id}", response_model=Categories)
def get_category_by_id(id: int,
                       db: Session= Depends(get_db),
                       userData: TokenData = Depends(auth.get_current_user)):
    category = db.query(Category).filter(Category.id == id)
    
    if userData.role != constants.ROLE_ADMIN:
        category = category.filter(Category.status == True)
        
    category = category.first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no category with id {id}!" 
        )
    
    return category

@router.post("/", response_model=List[Categories], status_code=status.HTTP_201_CREATED)
def create_categories(categories: List[CategoryCreate],
                      db: Session = Depends(get_db),
                      userData: TokenData = Depends(auth.get_current_user)):
    
    if userData.role != constants.ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized" 
        )
        
    db_categories = [Category(**category.dict()) for category in categories]
    db.add_all(db_categories)
    db.commit()
    return db_categories

@router.patch("/", status_code=status.HTTP_202_ACCEPTED)
def update_categories(categories: List[CategoryUpdate],
                      db: Session = Depends(get_db),
                      userData: TokenData = Depends(auth.get_current_user)):    
    if userData.role != constants.ROLE_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized")

    for category in categories:
        db_category = db.query(Category).filter(Category.id == category.id).first()
        
        if not db_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Category not found")
        
        [setattr(db_category, key, value) for key, value in category.dict(exclude_unset=True).items()]

        db_category.update_at = func.now()
                
    db.commit()
    return {"detail": "Categories updated successfully"}

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_categories(id: List[int],
                      db : Session = Depends(get_db),
                      userData: TokenData = Depends(auth.get_current_user)):
    if userData.role != constants.ROLE_ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized")
    
    categories = db.query(Category).filter(Category.id.in_(id)).all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No categories found with the provided IDs")

    for category in categories:
        if category.status == True:
            category.status = False
            category.update_at = func.now()
        
    db.commit()
    
    return {"detail": "Categories deleted"}