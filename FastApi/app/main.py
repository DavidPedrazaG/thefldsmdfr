"""
main.py

This is the main entry point for the FastAPI application. It handles the initialization of 
the app, setting up the lifespan context, and registering API routes for movies and plants.

The application connects to the database at startup, creates necessary tables if they 
don't exist, and ensures that the database connection is closed properly upon shutdown.
"""
# pylint: disable=E0401
# Standard library imports
from contextlib import asynccontextmanager

# Local imports (from your project)
from helpers.api_key_auth import get_api_key
from database import database as connection
from database import (
    PlantModel, PlantTypeModel, MovieModel, GenreModel, PersonModel, MoviePersonModel
)
from routes.movie_routes import movie_router, person_router, genre_router
from routes.plant_routes import plant_route

# Third-party imports
from fastapi import Depends, FastAPI


# Lifespan context manager to handle the lifecycle of the FastAPI app
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Manages the lifespan of the FastAPI app. It ensures that the database connection 
    is opened at the start of the app's lifecycle and closed when the app shuts down.

    Args:
        _app (FastAPI): The FastAPI instance.

    Yields:
        None
    """
    if connection.is_closed():
        connection.connect()
        connection.create_tables([
            PlantModel, PlantTypeModel, MovieModel, GenreModel,
            PersonModel, MoviePersonModel
        ])

    try:
        yield

    finally:
        if not connection.is_closed():
            connection.close()


# Initialize the FastAPI application with the custom lifespan function
app = FastAPI(lifespan=lifespan)

# API KEY Validation
@app.get("/protected-endpoint")
async def protected_endpoint(api_key: str = Depends(get_api_key)):
    """
    Protected endpoint that requires a valid API key for access.

    This function handles requests to the `/protected-endpoint` route. 
    It validates the API key provided in the request's security header using the 
    `get_api_key` function. If the API key is valid, the function grants access 
    to the protected resource.

    Args:
        api_key (str): The API key extracted and validated using the `get_api_key` dependency.

    Returns:
        dict: A message indicating access to the protected endpoint with the valid API key.
    """
    return {"message": f"Acceso concedido a endpoint protegido con el key{api_key}"}

# Register the movie-related routes
app.include_router(movie_router, prefix="/api/movies",
                   tags=["movies"], dependencies=[Depends(get_api_key)])
app.include_router(genre_router, prefix="/api/genre", tags=["genre"],
                   dependencies=[Depends(get_api_key)])
app.include_router(person_router, prefix="/api/person", tags=["persons"],
                   dependencies=[Depends(get_api_key)])

# Register the plant-related routes
app.include_router(plant_route, prefix="/api/plants", tags=["plants"],
                   dependencies=[Depends(get_api_key)])
