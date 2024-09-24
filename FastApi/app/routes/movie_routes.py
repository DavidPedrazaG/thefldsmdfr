"""
movie_routes.py

This module defines the API endpoints for managing movies, genres, and people 
in the film industry using FastAPI. It includes endpoints for creating, 
reading, updating, and deleting records in the database.
"""
# pylint: disable=E0401
from schemas.movie_schema import Movie
from schemas.genre_schema import Genre
from schemas.person_schema import Person
from database import MovieModel, GenreModel, PersonModel, MoviePersonModel
from fastapi import APIRouter, Body, HTTPException

# Initialize routers for movies, genres, and people
movie_router = APIRouter()
genre_router = APIRouter()
person_router = APIRouter()

# Movie Endpoints
@movie_router.post("/")
async def create_movie(movie: Movie = Body(...)):
    """Create a new movie in the database."""
    new_movie = MovieModel.create(
        title=movie.title,
        director=movie.director,
        release_year=movie.release_year,
        duration=movie.duration,
        genre=movie.genre,
        country_of_origin=movie.country_of_origin,
    )
    for person_id in movie.cast:
        MoviePersonModel.create(
            movie_id=new_movie.id,
            person_id=person_id
        )
    return {"message": "Movie created successfully"}

@movie_router.get("/")
async def read_movies():
    """Retrieve a list of all movies from the database."""
    movies = []
    for movie in MovieModel.select():
        cast_ids = [
            mp[0] for mp in MoviePersonModel.select(MoviePersonModel.person_id).where(
                MoviePersonModel.movie_id == movie.id
            ).tuples()
        ]
        movies.append(Movie(
            id=movie.id,
            title=movie.title,
            director=movie.director.id,
            release_year=movie.release_year,
            duration=movie.duration,
            genre=movie.genre.id,
            country_of_origin=movie.country_of_origin,
            cast=cast_ids
        ))
    return movies

@movie_router.get("/{movie_id}")
async def read_movie(movie_id: int):
    """Retrieve a specific movie by its ID, including cast IDs."""
    try:
        movie = MovieModel.get(MovieModel.id == movie_id)
        cast_ids = [
            mp[0] for mp in MoviePersonModel.select(MoviePersonModel.person_id).where(
                MoviePersonModel.movie_id == movie.id
            ).tuples()
        ]
        return Movie(
            id=movie.id,
            title=movie.title,
            director=movie.director.id,
            release_year=movie.release_year,
            duration=movie.duration,
            genre=movie.genre.id,
            country_of_origin=movie.country_of_origin,
            cast=cast_ids
        )
    except Exception as exc:  # catch all exception
        raise HTTPException(status_code=404, detail="Movie not found") from exc

@movie_router.put("/{movie_id}")
async def update_movie(movie_id: int, movie: Movie = Body(...)):
    """Update an existing movie by its ID."""
    try:
        movie_to_update = MovieModel.get(MovieModel.id == movie_id)
        movie_to_update.title = movie.title
        movie_to_update.director = movie.director
        movie_to_update.release_year = movie.release_year
        movie_to_update.duration = movie.duration
        movie_to_update.genre = movie.genre
        movie_to_update.country_of_origin = movie.country_of_origin
        MoviePersonModel.delete().where(MoviePersonModel.movie_id == movie_id).execute()
        for person_id in movie.cast:
            MoviePersonModel.create(
                movie_id=movie_id,
                person_id=person_id
            )
        movie_to_update.save()
        return {"message": "Movie updated successfully"}
    except Exception as exc:  # catch all exception
        raise HTTPException(status_code=404, detail="Movie not found") from exc

@movie_router.delete("/{movie_id}")
async def delete_movie(movie_id: int):
    """Delete a specific movie by its ID."""
    rows_deleted = MovieModel.delete().where(MovieModel.id == movie_id).execute()
    if rows_deleted:
        return {"message": "Movie deleted successfully"}
    raise HTTPException(status_code=404, detail="Movie not found")

# Genre Endpoints
@genre_router.post("/")
async def create_genre(genre: Genre = Body(...)):
    """Create a new genre in the database."""
    GenreModel.create(name=genre.name)
    return {"message": "Genre created successfully"}

@genre_router.get("/")
async def read_genres():
    """Retrieve a list of all genres from the database."""
    genres = GenreModel.select().dicts()
    return list(genres)

@genre_router.get("/{genre_id}")
async def read_genre(genre_id: int):
    """Retrieve a specific genre by its ID."""
    try:
        genre = GenreModel.get(GenreModel.id == genre_id)
        return genre
    except Exception as exc:  # catch all exception
        raise HTTPException(status_code=404, detail="Genre not found") from exc

@genre_router.put("/{genre_id}")
async def update_genre(genre_id: int, genre: Genre = Body(...)):
    """Update an existing genre by its ID."""
    try:
        genre_to_update = GenreModel.get(GenreModel.id == genre_id)
        genre_to_update.name = genre.name
        genre_to_update.save()
        return {"message": "Genre updated successfully"}
    except Exception as exc:  # catch all exception
        raise HTTPException(status_code=404, detail="Genre not found") from exc

@genre_router.delete("/{genre_id}")
async def delete_genre(genre_id: int):
    """Delete a specific genre by its ID."""
    rows_deleted = GenreModel.delete().where(GenreModel.id == genre_id).execute()
    if rows_deleted:
        return {"message": "Genre deleted successfully"}
    raise HTTPException(status_code=404, detail="Genre not found")

# Person Endpoints
@person_router.post("/")
async def create_person(person: Person = Body(...)):
    """Create a new person in the database."""
    PersonModel.create(
        name=person.name,
        age=person.age,
        role=person.role
    )
    return {"message": "Person created successfully"}

@person_router.get("/")
async def read_people():
    """Retrieve a list of all people from the database."""
    people = PersonModel.select().dicts()
    return list(people)

@person_router.get("/{person_id}")
async def read_person(person_id: int):
    """Retrieve a specific person by their ID."""
    try:
        person = PersonModel.get(PersonModel.id == person_id)
        return person
    except Exception as exc:  # catch all exception
        raise HTTPException(status_code=404, detail="Person not found") from exc

@person_router.put("/{person_id}")
async def update_person(person_id: int, person: Person = Body(...)):
    """Update an existing person by their ID."""
    try:
        person_to_update = PersonModel.get(PersonModel.id == person_id)
        person_to_update.name = person.name
        person_to_update.age = person.age
        person_to_update.role = person.role
        person_to_update.save()
        return {"message": "Person updated successfully"}
    except Exception as exc:  # catch all exception
        raise HTTPException(status_code=404, detail="Person not found") from exc

@person_router.delete("/{person_id}")
async def delete_person(person_id: int):
    """Delete a specific person by their ID."""
    rows_deleted = PersonModel.delete().where(PersonModel.id == person_id).execute()
    if rows_deleted:
        return {"message": "Person deleted successfully"}
    raise HTTPException(status_code=404, detail="Person not found")
