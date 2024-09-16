from pydantic import BaseModel ,Field , validator


class Plant_model(BaseModel):
    """Model representing a plant."""
    id: int
    scientific_name: str
    common_name: str
    plant_type: int  
    watering_needs: str
    ideal_temperature: float = Field(..., gt=0)  
    description: str | None = None  
    
    @validator("ideal_temperature")
    def temperature_must_be_positive(cls, v):
        """Ensure temperature is greater than 0."""
        if v <= 0:
            raise ValueError("Temperature must be positive")
        return v