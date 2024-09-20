"""
database.py

This module sets up the database connection using Peewee ORM and defines 
the data models for the application. It loads environment variables for 
database credentials using dotenv and creates models for plants, genres, 
people, movies, and their relationships.
"""

# Standard library imports
import os

# Third-party imports
from dotenv import load_dotenv
from peewee import Model, MySQLDatabase, AutoField, CharField
from peewee import ForeignKeyField, IntegerField, DecimalField, TextField

# Load environment variables from .env file
load_dotenv()

# Database configuration using MySQL
database = MySQLDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST')
)

class PlantTypeModel(Model):
    """Model representing a type of plant."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    # pylint: disable=R0903
    class Meta:
        """Database configuration for PlantTypeModel"""
        database = database
        table_name = "plant_types"

class PlantModel(Model):
    """Model representing a plant."""
    id = AutoField(primary_key=True)
    scientific_name = CharField(max_length=50)
    common_name = CharField(max_length=50)
    plant_type = ForeignKeyField(PlantTypeModel, backref='plants')
    watering_needs = CharField(max_length=50)
    ideal_temperature = DecimalField(max_digits=5, decimal_places=2)
    description = TextField(null=True)
    # pylint: disable=R0903
    class Meta:
        """Database configuration for PlantModel"""
        database = database
        table_name = "plants"

class GenreModel(Model):
    """Model representing a movie genre."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    # pylint: disable=R0903
    class Meta:
        """Database configuration for GenreModel"""
        database = database
        table_name = "genres"

class PersonModel(Model):
    """Model representing a person in the film industry."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    age = IntegerField()
    role = CharField(max_length=50)
    # pylint: disable=R0903
    class Meta:
        """Database configuration for PersonModel"""
        database = database
        table_name = "people"

class MovieModel(Model):
    """Model representing a movie."""
    id = AutoField(primary_key=True)
    title = CharField(max_length=100)
    director = ForeignKeyField(PersonModel, backref='movies')
    release_year = IntegerField()
    duration = IntegerField()
    genre = ForeignKeyField(GenreModel, backref='movies')
    country_of_origin = CharField(max_length=50)
    # pylint: disable=R0903
    class Meta:
        """Database configuration for MovieModel"""
        database = database
        table_name = "movies"

class MoviePersonModel(Model):
    """Model representing the relationship between a movie and a person."""
    movie_id = ForeignKeyField(MovieModel, backref='movie_person')
    person_id = ForeignKeyField(PersonModel, backref='movie_person')
    # pylint: disable=R0903
    class Meta:
        """Database configuration for MoviePersonModel"""
        database = database
        table_name = "movie_person"
