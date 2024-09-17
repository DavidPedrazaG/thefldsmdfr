from fastapi import APIRouter, Body, HTTPException
from schemas.movie_schema import Movie
from schemas.genre_schema import Genre
from schemas.person_schema import Person
from database import MovieModel, GenreModel, PersonModel

movie_router = APIRouter()
genre_router = APIRouter()
person_router = APIRouter()

# Movie Endpoints
@movie_router.post("/")
async def create_movie(movie: Movie = Body(...)):
    MovieModel.create(
        title=movie.title,
        description=movie.description,
        release_date=movie.release_date,
        genre_id=movie.genre_id,
        director_id=movie.director_id
    )
    return {"message": "Movie created successfully"}

@movie_router.get("/")
async def read_movies():
    movies = MovieModel.select().dicts()
    return list(movies)

@movie_router.get("/{movie_id}")
async def read_movie(movie_id: int):
    try:
        movie = MovieModel.get(MovieModel.id == movie_id)
        return movie
    except MovieModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie not found")

@movie_router.put("/{movie_id}")
async def update_movie(movie_id: int, movie: Movie = Body(...)):
    try:
        movie_to_update = MovieModel.get(MovieModel.id == movie_id)
        movie_to_update.title = movie.title
        movie_to_update.description = movie.description
        movie_to_update.release_date = movie.release_date
        movie_to_update.genre_id = movie.genre_id
        movie_to_update.director_id = movie.director_id
        movie_to_update.save()
        return {"message": "Movie updated successfully"}
    except MovieModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Movie not found")

@movie_router.delete("/{movie_id}")
async def delete_movie(movie_id: int):
    rows_deleted = MovieModel.delete().where(MovieModel.id == movie_id).execute()
    if rows_deleted:
        return {"message": "Movie deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Movie not found")

# Genre Endpoints
@genre_router.post("/")
async def create_genre(genre: Genre = Body(...)):
    GenreModel.create(name=genre.name)
    return {"message": "Genre created successfully"}

@genre_router.get("/")
async def read_genres():
    genres = GenreModel.select().dicts()
    return list(genres)

@genre_router.get("/{genre_id}")
async def read_genre(genre_id: int):
    try:
        genre = GenreModel.get(GenreModel.id == genre_id)
        return genre
    except GenreModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Genre not found")

@genre_router.put("/{genre_id}")
async def update_genre(genre_id: int, genre: Genre = Body(...)):
    try:
        genre_to_update = GenreModel.get(GenreModel.id == genre_id)
        genre_to_update.name = genre.name
        genre_to_update.save()
        return {"message": "Genre updated successfully"}
    except GenreModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Genre not found")

@genre_router.delete("/{genre_id}")
async def delete_genre(genre_id: int):
    rows_deleted = GenreModel.delete().where(GenreModel.id == genre_id).execute()
    if rows_deleted:
        return {"message": "Genre deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Genre not found")

# Person Endpoints
@person_router.post("/")
async def create_person(person: Person = Body(...)):
    PersonModel.create(
        first_name=person.first_name,
        last_name=person.last_name,
        birth_date=person.birth_date,
        role=person.role
    )
    return {"message": "Person created successfully"}

@person_router.get("/")
async def read_people():
    people = PersonModel.select().dicts()
    return list(people)

@person_router.get("/{person_id}")
async def read_person(person_id: int):
    try:
        person = PersonModel.get(PersonModel.id == person_id)
        return person
    except PersonModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Person not found")

@person_router.put("/{person_id}")
async def update_person(person_id: int, person: Person = Body(...)):
    try:
        person_to_update = PersonModel.get(PersonModel.id == person_id)
        person_to_update.first_name = person.first_name
        person_to_update.last_name = person.last_name
        person_to_update.birth_date = person.birth_date
        person_to_update.role = person.role
        person_to_update.save()
        return {"message": "Person updated successfully"}
    except PersonModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Person not found")

@person_router.delete("/{person_id}")
async def delete_person(person_id: int):
    rows_deleted = PersonModel.delete().where(PersonModel.id == person_id).execute()
    if rows_deleted:
        return {"message": "Person deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Person not found")
