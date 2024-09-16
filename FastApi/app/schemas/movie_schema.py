"""Esquemas para los modelos relacionados con películas en la aplicación."""
from typing import List
from pydantic import BaseModel, Field, validator

class MovieModel(BaseModel):
    """Modelo que representa una película."""
    id: int
    title: str
    director: int
    release_year: int
    duration: int = Field(..., gt=0)
    genre: int
    country_of_origin: str
    cast: List[int]
    @validator("release_year")
    def valid_release_year(self, v):
        """Asegurarse de que el año de lanzamiento sea válido."""
        if v < 1888:
            raise ValueError("El año de lanzamiento debe ser 1888 o posterior")
        return v
