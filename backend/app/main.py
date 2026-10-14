from app.db.models import Base
from app.db.session import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.orders import router as orders_router
from app.api.auth import router as auth_router

Base.metadata.create_all(bind=engine)
    
app = FastAPI(title="ShopAgent AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(orders_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}