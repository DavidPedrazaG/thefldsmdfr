"""Schemas for models related to movies in the application."""
from typing import List
from pydantic import BaseModel, Field, validator

class Movie(BaseModel):
    """Model representing a movie."""
    id: int
    title: str
    director: int
    release_year: int
    duration: int = Field(..., gt=0)
    genre: int
    country_of_origin: str
    cast: List[int]

    # pylint: disable=E0213
    @validator("release_year")
    def valid_release_year(cls, v):
        """Ensure that the release year is valid."""
        if v < 1888:
            raise ValueError("The release year must be 1888 or later")
        return v
