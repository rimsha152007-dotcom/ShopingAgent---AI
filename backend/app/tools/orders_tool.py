from datetime import datetime, timedelta
from typing import Dict, Any 
from sqlalchemy.orm import Session 
from app.db.models import Order, ActionLog, OrderStatus

# Helper function jo ActionLog table mein audit entry add karta hai
def log_action(db: Session, order_id: int, action_type: str, details: str):
    log = ActionLog(
        order_id=order_id,
        action_type=action_type,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()

# tool 1 order status check krna 
def get_order_status(db: Session, user_id: int, order_id: int) -> Dict[str, Any]:
    order=db.query(Order).filter(Order.id == order_id).first() #db sey order fetch ho raha 

    # Validation 1 order exist krta he ya nhi 
    if not order:
        return {"status":"error", "message": f"Order {order_id} not found"}
    # checking the order's owner 
    if order.user_id != user_id:
         return {"status":"error", "message": "unaurhorized aceess to this order"}
    # Audit log entry create karte hain 
    log_action(db, order.id, "CHECK_STATUS",f"Checked status: {Order.status}")

    return{
        "status":"success",
        "data":{
            "order_id": order.id,
            "order_status": Order.status,
            "items": order.items,
            "total_amount": order.total_amount
        }
    }

# tool 2 : shipping Adress update krna 
def update_shipping_address(db: Session, user_id: int, order_id: int, new_address: str) -> Dict[str, Any]:
    order = db.query(Order).filters(Order.id == order_id).first()

    if not order:
        return{"status":"error", "message": f"Order {order_id} not found"}

    if order.user_id != user_id:
         return{"status":"error", "message": "unauthorized access to this order"}

    # bussiness rule: shipped ya deliver order ka address change nhi ho sakta 
    if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED,OrderStatus.CANCELLED]:
         return{"status":"error", "message": f" Cannot update address for Order with status {order.status}"}

    # Adrress update krna 
    old_address = order.user.address if order.user else "N/A"
    if order.user:
        order.user.address = new_address
        db.commit()

    log_action(db, order.id, "UPDATE_ADDRESS", F"Updated address from {old_address} to {new_address}")

    return {"status": "success", "message": f"Shipping address updated for Order {order_id} updated sucessfully"}


# Tool 3: Order Cancel Karna
def cancel_order(db: Session, user_id: int, order_id: int, confirmed: bool = False, confirmation_token: str = None) -> Dict[str, Any]:
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        return {"status": "error", "message": f"Order {order_id} not found."}
    
    if order.user_id != user_id:
        return {"status": "error", "message": "Unauthorized access to this order."}
    
    # Business Rule 1: Agar order pehle hi shipped ho chuka ho
    if order.status == OrderStatus.SHIPPED:
        return {"status": "error", "message": "Cannot cancel an order that is already shipped."}
    
    if order.status == OrderStatus.CANCELLED:
        return {"status": "error", "message": "Order is already cancelled."}
    
    # Business Rule 2: Order creation ke 2 ghante baad cancellation allowed nahi hai
    time_limit = datetime.utcnow() - timedelta(hours=2)
    if order.created_at and order.created_at < time_limit:
        return {"status": "error", "message": "Orders can only be cancelled within 2 hours of creation."}
    
    # Cancel status set karein
    order.status = OrderStatus.CANCELLED
    db.commit()
    
    log_action(db, order.id, "CANCEL_ORDER", "Order cancelled successfully by user.")
    
    return {"status": "success", "message": f"Order {order_id} has been successfully cancelled."}
        
        



    