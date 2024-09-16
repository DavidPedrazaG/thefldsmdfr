from pydantic import BaseModel,Field , validator


class Person_model(BaseModel):
    """Model representing a person in the film industry."""
    id: int
    name: str
    age: int = Field(..., gt=0, le=100)  
    role: str
    
    @validator("age")
    def age_must_be_positive(cls, v):
        """Ensure age is positive."""
        if v < 0:
            raise ValueError("Age must be positive")
        return v