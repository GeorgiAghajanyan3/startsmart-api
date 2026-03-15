# Import SQLAlchemy column types
from sqlalchemy import Column, Integer, String

# Import Base class from database configuration
from database import Base


# Define Idea table model
class Idea(Base):

    # Name of the table in the database
    __tablename__ = "ideas"

    # Primary key column
    id = Column(Integer, primary_key=True, index=True)

    # Business idea title
    idea = Column(String, index=True)

    # Description of the idea
    description = Column(String)