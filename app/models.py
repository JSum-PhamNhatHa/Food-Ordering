from sqlalchemy import Boolean, Column, UUID, String
from .database import Base

class Temp(Base):
    __tablename__ = "temp-posts"
    
    id = Column(UUID, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    published = Column(Boolean, server_default='TRUE')
    