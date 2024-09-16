from pydantic import BaseModel ,Field , validator
from typing import List

class Movie_model(BaseModel):
    """Model representing a movie."""
    id: int
    title: str
    director: int  
    release_year: int
    duration: int = Field(..., gt=0) 
    genre: int  
    country_of_origin: str
    cast: List[int]  
    
    @validator("release_year")
    def valid_release_year(cls, v):
        """Ensure the release year is reasonable."""
        if v < 1888: 
            raise ValueError("Release year must be 1888 or later")
        return v