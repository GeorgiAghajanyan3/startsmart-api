# Import SQLAlchemy tools
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file
DATABASE_URL = "sqlite:///./startsmart.db"

# Create database engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create database session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for models
Base = declarative_base()