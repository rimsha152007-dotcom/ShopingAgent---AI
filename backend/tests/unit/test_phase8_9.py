import pytest
import time 
from app.db.session import SessionLocal
from app.tools.orders_tool import get_order_status, update_shipping_address, cancel_order
from app.llm.factory import get_llm_client
from app.llm.base import FakeClient
from app.db.models import User, Order, OrderStatus
from app.core.security import get_password_hash

# Test 1: LLM Factory & FakeClient Test
def test_fake_llm_client():
    client = get_llm_client()
    # Check karein ke factory 'fake' provider par sahi client return kar rahi hai
    assert isinstance(client, FakeClient)
    
    response = client.generate_response([{"role": "user", "content": "What is my order status?"}])
    assert "status" in response.lower() or "pending" in response.lower()

# Test 2: Tools Authorization & Wrong Owner Test
def test_tool_unauthorized_access():
    db = SessionLocal()
    try:
        unique_email = f"owner_{int(time.time())}@test.com"
        
        owner = User(full_name="Owner User", email=unique_email, hashed_password=get_password_hash("123"), address="Lahore")
        db.add(owner)
        db.commit()
        db.refresh(owner)

        order = Order(user_id=owner.id, items="Test Item", total_amount=100.0, status=OrderStatus.PENDING)
        db.add(order)
        db.commit()
        db.refresh(order)

        result = get_order_status(db=db, user_id=999, order_id=order.id)
        
        assert result["status"] == "error"
        assert "unaurhorized" in result["message"].lower()
    finally:
        db.close()

# Test 3: Tool Order Not Found Test
def test_tool_order_not_found():
    db = SessionLocal()
    try:
        # Aisi order ID pass karein jo exist hi nahi karti
        result = cancel_order(db=db, user_id=1, order_id=99999)
        
        assert result["status"] == "error"
        assert "not found" in result["message"]
    finally:
        db.close()