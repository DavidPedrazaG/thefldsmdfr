"""Esquemas para los modelos relacionados con generos de las peliculas en la aplicación."""
from pydantic import BaseModel


class Genre(BaseModel):
    """Model representing a genre."""
    id: int
    name: str
