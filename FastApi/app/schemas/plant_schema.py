"""Schemas for models related to plants in the application."""
from pydantic import BaseModel, Field, validator

class Plant(BaseModel):
    """Model representing a plant."""
    id: int
    scientific_name: str
    common_name: str
    plant_type: int
    watering_needs: str
    ideal_temperature: float = Field(..., gt=0)
    description: str | None = None

    # pylint: disable=E0213
    @validator("ideal_temperature")
    def temperature_must_be_positive(cls, v):
        """Ensure temperature is positive."""
        if v <= 0:
            raise ValueError("Temperature must be positive")
        return v
