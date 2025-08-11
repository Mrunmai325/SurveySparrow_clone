from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base 
# SQLite connection (no dependencies needed)
engine = create_engine("sqlite:///survey.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)# database/__init__.py
 # Your SQLAlchemy models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
