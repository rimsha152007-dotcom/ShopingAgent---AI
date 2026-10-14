import enum 
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class OrderStatus(str, enum.Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    address = Column(String, nullable=True)

    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    items = Column(String, nullable=False)  # JSON or comma-separated items
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    logs = relationship("ActionLog", back_populates="order")

class ActionLog(Base):
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    action_type = Column(String, nullable=False)  # e.g., "CANCEL_ORDER", "UPDATE_ADDRESS"
    details = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="logs")    
