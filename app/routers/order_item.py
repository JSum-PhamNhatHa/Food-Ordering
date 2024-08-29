from fastapi import Depends, HTTPException, status, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from ..models.database import get_db
from app.models.tables import OrderItem, Menu, Order
from app.schemas.user import TokenData
from app.schemas.order import Orders
from app.schemas.order_item import Items, ItemCreate, ItemUpdate
from ..utils import auth, constants

router = APIRouter(prefix="/orders", tags=["Order"])

def forbidden_cust(userData: TokenData = Depends(auth.get_current_user)):
    if userData.role == constants.ROLE_CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

def update_order_totals(order_id: int, db: Session):
    quantity = db.query(func.sum(OrderItem.quantity)).filter(OrderItem.order_id == order_id).scalar()
    total = db.query(func.sum(OrderItem.total)).filter(OrderItem.order_id == order_id).scalar()
    return quantity, total


@router.post("/{order_id}", response_model=List[Orders], status_code=status.HTTP_201_CREATED)
def create_order_items(order_id: int,
                       items: List[ItemCreate],
                       db: Session = Depends(get_db),
                       userData: TokenData = Depends(auth.get_current_user)):
    forbidden_cust(userData)
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found!"
        )
        
    for item in items:
        menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with id {item.menu_id} not found!"
            )
        
        total = item.quantity * menu.price
        
        db_item = OrderItem(
            order_id=order_id,
            menu_id=item.menu_id,
            quantity=item.quantity,
            price=menu.price,
            total=total,
            user_id=userData.id
        )
        
        db.add(db_item)
        db_order_items.append(db_item)
        
    db_order.quantity, db_order.total = update_order_totals(order_id, db)
    db.commit()
    
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    # Return the order with its items
    return [Orders(
        id=order.id,
        quantity=order.quantity,
        total=order.total,
        status=order.status,
        user_id=order.user_id,
        items=order_items
    )]
    
@router.patch("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_order_item_quantity(order_id: int,
                               item: ItemUpdate,
                               db : Session = Depends(get_db),
                               userData: TokenData = Depends(auth.get_current_user),
                               ):
    forbidden_cust(userData)
    
    db_order = db.query(Order).filter(Order.id == order_id).first()
    
    if not db_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found!"
        )
        
    db_item = db.query(OrderItem).filter(OrderItem.order_id == order_id,
                                                  OrderItem.id == item.id).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found"
        )
    
    db_item.quantity = item.quantity
    db_item.total = db_item.quantity * db_item.price
    db_item.updated_at = func.now()
    
    db_order.quantity, db_order.total = update_order_totals(order_id, db)
    db.commit()
    
    return {"detail": "Order updated successfully"}  

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_items(order_id: int,
                       id: List[int],
                       db : Session = Depends(get_db),
                       userData: TokenData = Depends(auth.get_current_user)):
    forbidden_cust(userData)
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found!"
        )
        
    items = db.query(OrderItem).filter(OrderItem.order_id == order_id,
                                       OrderItem.id.in_(id)).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No items found with the provided IDs")

    for item in items:
        db.delete(item)
        
    db_order.quantity, db_order.total = update_order_totals(order_id, db)
    db.commit()
    
    return {"detail": "Order items deleted"}