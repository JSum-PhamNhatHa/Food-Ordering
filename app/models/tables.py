import uuid
from sqlalchemy import TIMESTAMP, Column, String, Text, Integer, ForeignKey, Boolean, Numeric
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    create_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now())
    
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="This is a food description.")
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    create_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now())
    
class Menu(Base):
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False, default="This is a dish description.")
    price = Column(Numeric(5,2), nullable=False, default=0.0)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    create_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now())
    
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(String, nullable=False)
    total = Column(Numeric(10,2), nullable=False, default=0.0)
    status = Column(Boolean, nullable=False, default=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    create_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now())
    
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(String, nullable=False)
    price = Column(Numeric(5,2), nullable=False, default=0.0)
    total = Column(Numeric(10,2), nullable=False, default=0.0)
    menu_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    create_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now())