from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Uses SQLite for local persistence without requiring SQL Server ODBC configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./performance.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()