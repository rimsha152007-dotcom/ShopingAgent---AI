import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your Base metadata
from app.db.models import Base  # Adjust import path if needed

config = context.config

# Connect using local Postgres by default, or DATABASE_URL env var
db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgrespassword@localhost:5432/app_db")
config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata