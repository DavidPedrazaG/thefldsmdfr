from pydantic import BaseModel

class Plant_type_model(BaseModel):
    """Model representing a plant type."""
    id: int
    name: str
