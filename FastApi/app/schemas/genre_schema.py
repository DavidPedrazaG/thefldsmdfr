from pydantic import BaseModel


class genre_model(BaseModel):
    """Model representing a genre."""
    id:int
    name:str