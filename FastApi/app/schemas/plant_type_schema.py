"""Schemas for models related to plant types in the application."""
from pydantic import BaseModel

class PlantType(BaseModel):
    """Model representing a plant type."""
    id: int
    name: str
