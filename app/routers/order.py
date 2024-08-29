from fastapi import Depends, HTTPException, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from ..models.database import get_db
from app.models.tables import Order, OrderItem
from app.schemas.user import TokenData
from app.schemas.order import Orders, OrderCreate
from ..utils import auth, constants

router = APIRouter(prefix="/orders", tags=["Order"])

def forbidden_cust(userData: TokenData = Depends(auth.get_current_user)):
    if userData.role == constants.ROLE_CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
        
@router.get("/", response_model=List[Orders])
def get_orders(db: Session = Depends(get_db), 
               userData: TokenData = Depends(auth.get_current_user),
               page_index: int = Query(1, ge=1),
               page_size: int = Query(10, le=100)):
    forbidden_cust(userData)
    
    query = db.query(Order)
        
    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No orders found!"
        )
    
    total_size = query.count()
    total_page = (total_size + page_size - 1) // page_size

    if page_index > total_page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page index out of range!"
        )

    page_skip = (page_index - 1) * page_size
    orders = query.offset(page_skip).limit(page_size).all()
    
    orders_with_items = []
    for order in orders:
        items = db.query(models.Items).filter(models.Items.order_id == order.id).all()
        orders_with_items.append(Orders(
            id=order.id,
            quantity=order.quantity,
            total=order.total,
            status=order.status,
            user_id=order.user_id,
            items=items
        ))
    
    return orders_with_items

@router.get("/{id}", response_model=Orders)
def get_order_by_id(id: int,
                    db: Session= Depends(get_db),
                    userData: TokenData = Depends(auth.get_current_user)):    
    order = db.query(Order).filter(Order.id == id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no order with id {id}!" 
        )
        
    items = db.query(OrderItem).filter(OrderItem.order_id == id).all()
    
    return Orders(
        id=order.id,
        quantity=order.quantity,
        total=order.total,
        status=order.status,
        user_id=order.user_id,
        items=items
    )

@router.post("/", response_model=List[Orders], status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate,
                 db: Session = Depends(get_db),
                 userData: TokenData = Depends(auth.get_current_user)):
    
    if userData.role != constants.ROLE_STAFF:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized" 
        )
         
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    return db_order

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_menus(id: List[int],
                 db : Session = Depends(get_db),
                 userData: TokenData = Depends(auth.get_current_user)):
    forbidden_cust(userData)
    
    orders = db.query(Order).filter(Order.id.in_(id)).all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No orders found with the provided IDs")

    for order in orders:
        if order.status == True:
            order.status = False
            order.update_at = func.now()
        
    db.commit()
    
    return {"detail": "Orders deleted"}