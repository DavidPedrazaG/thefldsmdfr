"""Esquemas para los modelos relacionados con plantas en la aplicación."""
from pydantic import BaseModel, Field, validator

class PlantModel(BaseModel):
    """Modelo que representa una planta."""
    id: int
    scientific_name: str
    common_name: str
    plant_type : int
    watering_needs: str
    ideal_temperature: float = Field(..., gt=0)
    description: str | None = None
    @validator("ideal_temperature")
    def temperature_must_be_positive(self, v):
        """_summary_

        Args:
            cls
            v (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if v <= 0:
            raise ValueError("La temperatura debe ser positiva")
        return v
