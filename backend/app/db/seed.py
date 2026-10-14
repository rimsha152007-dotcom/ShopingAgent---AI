from datetime import datetime, timedelta
from app.db.session import engine, SessionLocal
from app.db.models import Base, User, Order, OrderStatus, ActionLog
from app.core.security import get_password_hash

def seed_database():
    # Tables create karein
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check karein agar orders pehle se majood hain
    if db.query(Order).first():
        print("Database mein orders pehle se seeded hain!")
        db.close()
        return

    print("Seeding database...")

    # Sample user dhoondhein ya naya create karein
    user1 = db.query(User).filter(User.email == "ali@example.com").first()
    if not user1:
        user1 = User(
            full_name="Ali Khan", 
            email="ali@example.com", 
            hashed_password=get_password_hash("password123"),
            address="Gulberg III, Lahore"
        )
        db.add(user1)
        db.commit()
        db.refresh(user1)

    user2 = db.query(User).filter(User.email == "sara@example.com").first()
    if not user2:
        user2 = User(
            full_name="Sara Ahmed", 
            email="sara@example.com", 
            hashed_password=get_password_hash("password123"),
            address="DHA Phase 5, Lahore"
        )
        db.add(user2)
        db.commit()
        db.refresh(user2)

    # Orders create karein
    now = datetime.utcnow()
    
    order1 = Order(
        user_id=user1.id,
        items="Laptop Bag, Wireless Mouse",
        total_amount=4500.0,
        status=OrderStatus.PENDING,
        created_at=now - timedelta(minutes=30)
    )
    
    order2 = Order(
        user_id=user1.id,
        items="Mechanical Keyboard",
        total_amount=8500.0,
        status=OrderStatus.SHIPPED,
        created_at=now - timedelta(hours=5)
    )

    order3 = Order(
        user_id=user2.id,
        items="USB-C Hub",
        total_amount=2200.0,
        status=OrderStatus.PENDING,
        created_at=now - timedelta(hours=2)
    )

    db.add_all([order1, order2, order3])
    db.commit()

    # Action Log entry
    log1 = ActionLog(
        order_id=order1.id,
        action_type="ORDER_CREATED",
        details="Order placed successfully by Ali Khan"
    )
    db.add(log1)
    db.commit()

    print("Database seeding completed successfully!")
    db.close()

if __name__ == "__main__":
    seed_database()