from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

engine = create_engine("sqlite:///survey.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
