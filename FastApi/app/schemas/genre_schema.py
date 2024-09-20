"""Schemas for models related to movie genres in the application."""
from pydantic import BaseModel

class Genre(BaseModel):
    """Model representing a genre."""
    id: int
    name: str
