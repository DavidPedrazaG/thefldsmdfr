from fastapi import APIRouter, Body, HTTPException
from schemas.movie_schema import Movie
from schemas.genre_schema import Genre
from schemas.person_schema import Person
from typing import List

# Initialize the router
router = APIRouter()

# In-memory data storage for demonstration purposes
movies = []
genres = []
people = []

# Create endpoints

# Movie Endpoints

@router.post("/movies/", response_model=Movie)
async def create_movie(movie: Movie = Body(...)):
    """Create a new movie"""
    movies.append(movie)
    return movie

@router.get("/movies/", response_model=List[Movie])
async def read_movies():
    """Read all movies"""
    return movies

@router.get("/movies/{movie_id}", response_model=Movie)
async def read_movie(movie_id: int):
    """Read a movie by ID"""
    for movie in movies:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@router.put("/movies/{movie_id}", response_model=Movie)
async def update_movie(movie_id: int, movie: Movie = Body(...)):
    """Update a movie"""
    for i, existing_movie in enumerate(movies):
        if existing_movie.id == movie_id:
            movies[i] = movie
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@router.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int):
    """Delete a movie"""
    for i, movie in enumerate(movies):
        if movie.id == movie_id:
            del movies[i]
            return {"message": "Movie deleted"}
    raise HTTPException(status_code=404, detail="Movie not found")

# Genre Endpoints

@router.post("/genres/", response_model=Genre)
async def create_genre(genre: Genre = Body(...)):
    """Create a new genre"""
    genres.append(genre)
    return genre

@router.get("/genres/", response_model=List[Genre])
async def read_genres():
    """Read all genres"""
    return genres

@router.get("/genres/{genre_id}", response_model=Genre)
async def read_genre(genre_id: int):
    """Read a genre by ID"""
    for genre in genres:
        if genre.id == genre_id:
            return genre
    raise HTTPException(status_code=404, detail="Genre not found")

@router.put("/genres/{genre_id}", response_model=Genre)
async def update_genre(genre_id: int, genre: Genre = Body(...)):
    """Update a genre"""
    for i, existing_genre in enumerate(genres):
        if existing_genre.id == genre_id:
            genres[i] = genre
            return genre
    raise HTTPException(status_code=404, detail="Genre not found")

@router.delete("/genres/{genre_id}")
async def delete_genre(genre_id: int):
    """Delete a genre"""
    for i, genre in enumerate(genres):
        if genre.id == genre_id:
            del genres[i]
            return {"message": "Genre deleted"}
    raise HTTPException(status_code=404, detail="Genre not found")

# Person Endpoints

@router.post("/people/", response_model=Person)
async def create_person(person: Person = Body(...)):
    """Create a new person"""
    people.append(person)
    return person

@router.get("/people/", response_model=List[Person])
async def read_people():
    """Read all people"""
    return people

@router.get("/people/{person_id}", response_model=Person)
async def read_person(person_id: int):
    """Read a person by ID"""
    for person in people:
        if person.id == person_id:
            return person
    raise HTTPException(status_code=404, detail="Person not found")

@router.put("/people/{person_id}", response_model=Person)
async def update_person(person_id: int, person: Person = Body(...)):
    """Update a person"""
    for i, existing_person in enumerate(people):
        if existing_person.id == person_id:
            people[i] = person
            return person
    raise HTTPException(status_code=404, detail="Person not found")

@router.delete("/people/{person_id}")
async def delete_person(person_id: int):
    """Delete a person"""
    for i, person in enumerate(people):
        if person.id == person_id:
            del people[i]
            return {"message": "Person deleted"}
    raise HTTPException(status_code=404, detail="Person not found")