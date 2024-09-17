from dotenv import load_dotenv
from peewee import *
import os

load_dotenv()

database = MySQLDatabase(
    os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST')
)

class PlantTypeModel(Model):
    """Model representing a plant type."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)

    class Meta:
        database = database
        table_name = "plant_types"

class PlantModel(Model):
    """Model representing a plant."""
    id = AutoField(primary_key=True)
    scientific_name = CharField(max_length=50)
    common_name = CharField(max_length=50)
    plant_type = ForeignKeyField(PlantTypeModel, related_name='plants')  
    watering_needs = CharField(max_length=50)
    ideal_temperature = DecimalField(max_digits=5, decimal_places=2)
    description = TextField(null=True)

    class Meta:
        database = database
        table_name = "plants"

class GenreModel(Model):
    """Model representing a genre."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)

    class Meta:
        database = database
        table_name = "genres"

class PersonModel(Model):
    """Model representing a person in the film industry."""
    id = AutoField(primary_key=True)
    name = CharField(max_length=100)
    age = IntegerField()
    role = CharField(max_length=50) 

    class Meta:
        database = database
        table_name = "people"

class MovieModel(Model):
    """Model representing a movie."""
    id = AutoField(primary_key=True)
    title = CharField(max_length=100)
    director = ForeignKeyField(PersonModel, related_name='movies')  # Relación con PersonModel
    release_year = IntegerField()
    duration = IntegerField()
    genre = ForeignKeyField(GenreModel, related_name='movies')  # Relación con GenreModel
    country_of_origin = CharField(max_length=50)

    class Meta:
        database = database
        table_name = "movies"

