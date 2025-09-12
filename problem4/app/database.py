from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: Configure database URL
DATABASE_URL = "postgresql://user:password@localhost/library_db"

# TODO: Create database engine
engine = None

# TODO: Create session factory
SessionLocal = None

# TODO: Create base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    # TODO: Implement database session management
    pass