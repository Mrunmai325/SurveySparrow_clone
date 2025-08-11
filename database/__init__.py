# database/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # Your SQLAlchemy models

# Initialize database
engine = create_engine("sqlite:///survey.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
