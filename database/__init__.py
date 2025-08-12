from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# For SQLite:
engine = create_engine('sqlite:///survey.db')
# For PostgreSQL:
# engine = create_engine('postgresql://user:password@localhost/dbname')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
