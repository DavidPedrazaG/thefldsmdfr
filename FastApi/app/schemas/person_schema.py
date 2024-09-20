"""Schemas for models related to people in the application."""
from pydantic import BaseModel, Field, validator

class Person(BaseModel):
    """Model representing a person in the film industry."""
    id: int
    name: str
    age: int = Field(..., gt=0, le=100)
    role: str

    # pylint: disable=E0213
    @validator("age")
    def age_must_be_positive(cls, v):
        """Ensure age is positive."""
        if v < 0:
            raise ValueError("Age must be positive")
        return v
