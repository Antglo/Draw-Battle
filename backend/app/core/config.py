# backend/app/core/config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Settings:
    PROJECT_NAME: str = "Drawing Battle Game"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "postgresql://draw_user:your_password@localhost/draw_battle"

settings = Settings()

# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
