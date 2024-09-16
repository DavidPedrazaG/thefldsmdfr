"""Esquemas para los modelos relacionados con tippos de plantas en la aplicación."""
from pydantic import BaseModel

class PlantTypeModel(BaseModel):
    """Model representing a plant type."""
    id: int
    name: str
