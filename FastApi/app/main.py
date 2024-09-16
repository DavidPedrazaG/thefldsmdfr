from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database as connection
from database import *

@asynccontextmanager
async def lifespan(app: FastAPI):

    if connection.is_closed():
        connection.connect()
        connection.create_tables([PlantModel, PlantTypeModel, MovieModel, GenreModel, PersonModel])

    try:
        yield

    finally:
        if not connection.is_closed():
            connection.close

app = FastAPI(lifespan = lifespan)