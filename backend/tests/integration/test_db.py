import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, User

# SQLite test database URL set karein
TEST_DB_URL = "sqlite:///./test.db"

@pytest.fixture
def db_session():
    # 1. SQLite engine create karta hai (check_same_thread threading errors rokne ke liye hai)
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    
    # 2. Test database ke andar saari tables create karta hai
    Base.metadata.create_all(bind=engine)
    
    # 3. Session factory banata hai jo database transactions handle karegi
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    
    # 4. Test ko session provide karta hai
    yield session
    
    # 5. Test complete hone ke baad session close aur tables clean kar deta hai
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db_session):
    # Test user object create karte hain
    new_user = User(
        full_name="Test User",
        email="testuser@example.com",
        hashed_password="fakehashedpassword",
        address="Lahore"
    )
    
    # Session mein add karke commit karte hain
    db_session.add(new_user)
    db_session.commit()
    
    # Database se user query karke verify karte hain ke save ho gaya hai
    retrieved_user = db_session.query(User).filter(User.email == "testuser@example.com").first()
    
    assert retrieved_user is not None
    assert retrieved_user.full_name == "Test User"