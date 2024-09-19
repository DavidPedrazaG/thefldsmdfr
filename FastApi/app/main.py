from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database as connection
from database import *
from routes.movie_routes import movie_router, person_router, genre_router
from routes.plant_routes import plant_route

@asynccontextmanager
async def lifespan(app: FastAPI):

    if connection.is_closed():
        connection.connect()
        connection.create_tables([PlantModel, PlantTypeModel, MovieModel, GenreModel, PersonModel, MoviePersonModel])

    try:
        yield

    finally:
        if not connection.is_closed():
            connection.close

app = FastAPI(lifespan = lifespan)

app.include_router(movie_router, prefix="/api/movies", tags={"movies"})
app.include_router(genre_router, prefix="/api/genre", tags={"genre"})
app.include_router(person_router, prefix="/api/person", tags={"persons"})
app.include_router(plant_route, prefix="/api/plants", tags={"plants"})
