from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_connection():
    """Returns a database connection."""
    return engine