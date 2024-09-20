"""
main.py

This is the main entry point for the FastAPI application. It handles the initialization of 
the app, setting up the lifespan context, and registering API routes for movies and plants.

The application connects to the database at startup, creates necessary tables if they 
don't exist, and ensures that the database connection is closed properly upon shutdown.
"""

# Standard library imports
from contextlib import asynccontextmanager

# Local imports (from your project)
from database import database as connection
from database import (
    PlantModel, PlantTypeModel, MovieModel, GenreModel, PersonModel, MoviePersonModel
)
from routes.movie_routes import movie_router, person_router, genre_router
from routes.plant_routes import plant_route

# Third-party imports
from fastapi import FastAPI


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

# Register the movie-related routes
app.include_router(movie_router, prefix="/api/movies", tags=["movies"])
app.include_router(genre_router, prefix="/api/genre", tags=["genre"])
app.include_router(person_router, prefix="/api/person", tags=["persons"])

# Register the plant-related routes
app.include_router(plant_route, prefix="/api/plants", tags=["plants"])
