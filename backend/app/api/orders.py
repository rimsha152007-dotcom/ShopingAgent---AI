from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.db.session import get_db
from app.db.models import Order, OrderStatus, ActionLog

router = APIRouter(prefix="/orders", tags=["orders"])

# pydantic schemas 
class OrderResponse(BaseModel):
    id:int
    user_id:int
    total_amount:float
    status:str

    class Config:
        from_attributes = True


class StatusUpdateSchema(BaseModel):
    status: OrderStatus

class AddressUpdateSchema(BaseModel):
    address: str   

# get all the orders 
@router.get("/", response_model=List[OrderResponse])
def get_orders(db:Session = Depends(get_db)):
    return db.query(Order).all()

# 2. Get Single Order by ID
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# 3. Cancel Order
@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status == OrderStatus.SHIPPED or order.status == OrderStatus.DELIVERED:
        raise HTTPException(status_code=400, detail="Cannot cancel order that is already shipped or delivered")
    
    order.status = OrderStatus.CANCELLED
    
    log = ActionLog(
        order_id=order.id,
        action_type="CANCEL_ORDER",
        details="Order cancelled via API"
    )
    db.add(log)
    db.commit()
    
    return {"message": "Order cancelled successfully", "order_id": order.id, "status": order.status}
     



                   