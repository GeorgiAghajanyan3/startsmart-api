# Import BaseModel from Pydantic
from pydantic import BaseModel


# Schema for creating an idea
class IdeaCreate(BaseModel):

    # Business idea title
    idea: str

    # Idea description
    description: str


# Schema for returning idea data
class IdeaResponse(BaseModel):

    id: int
    idea: str
    description: str

    class Config:
        from_attributes = True