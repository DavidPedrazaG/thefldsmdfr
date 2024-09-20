"""Schemas for models related to plants in the application."""
from schemas.plant_schema import Plant
from schemas.plant_type_schema import PlantType
from database import PlantModel, PlantTypeModel
from fastapi import APIRouter, Body, HTTPException


plant_route = APIRouter()

# Create Plant
@plant_route.post("/")
async def create_plant(plant: Plant = Body(...)):
    """Create a new plant in the database."""
    PlantModel.create(
        scientific_name=plant.scientific_name,
        common_name=plant.common_name,
        plant_type=plant.plant_type,
        watering_needs=plant.watering_needs,
        ideal_temperature=plant.ideal_temperature,
        description=plant.description
    )
    return {"message": "Plant created successfully"}

# Read All Plants
@plant_route.get("/")
async def read_all_plants():
    """Retrieve a list of all plants."""
    plants = PlantModel.select().dicts()
    return list(plants)

# Read Plant by ID
@plant_route.get("/{plant_id}")
async def read_plant(plant_id: int):
    """Retrieve a specific plant by its ID."""
    try:
        plant = PlantModel.get(PlantModel.id == plant_id)
        return plant
    except Exception as exc:  # Catch all exceptions
        raise HTTPException(status_code=404, detail="Plant not found") from exc

# Update Plant
@plant_route.put("/{plant_id}")
async def update_plant(plant_id: int, plant: Plant = Body(...)):
    """Update an existing plant's information."""
    try:
        existing_plant = PlantModel.get(PlantModel.id == plant_id)
        existing_plant.scientific_name = plant.scientific_name
        existing_plant.common_name = plant.common_name
        existing_plant.plant_type = plant.plant_type
        existing_plant.watering_needs = plant.watering_needs
        existing_plant.ideal_temperature = plant.ideal_temperature
        existing_plant.description = plant.description
        existing_plant.save()
        return {"message": "Plant updated successfully"}
    except Exception as exc:  # Catch all exceptions
        raise HTTPException(status_code=404, detail="Plant not found") from exc

# Delete Plant
@plant_route.delete("/{plant_id}")
async def delete_plant(plant_id: int):
    """Delete a plant from the database by its ID."""
    rows_deleted = PlantModel.delete().where(PlantModel.id == plant_id).execute()
    if rows_deleted:
        return {"message": "Plant deleted successfully"}
    raise HTTPException(status_code=404, detail="Plant not found")

# Create Plant Type
@plant_route.post("/plant-types/")
async def create_plant_type(plant_type: PlantType = Body(...)):
    """Create a new plant type."""
    PlantTypeModel.create(
        name=plant_type.name
    )
    return {"message": "Plant type created successfully"}

# Read All Plant Types
@plant_route.get("/plant-types/")
async def read_all_plant_types():
    """Retrieve a list of all plant types."""
    plant_types = PlantTypeModel.select().dicts()
    return list(plant_types)

# Read Plant Type by ID
@plant_route.get("/plant-types/{plant_type_id}")
async def read_plant_type(plant_type_id: int):
    """Retrieve a specific plant type by its ID."""
    try:
        plant_type = PlantTypeModel.get(PlantTypeModel.id == plant_type_id)
        return plant_type
    except Exception as exc:  # Catch all exceptions
        raise HTTPException(status_code=404, detail="Plant type not found") from exc

# Update Plant Type
@plant_route.put("/plant-types/{plant_type_id}")
async def update_plant_type(plant_type_id: int, plant_type: PlantType = Body(...)):
    """Update an existing plant type's information."""
    try:
        existing_plant_type = PlantTypeModel.get(PlantTypeModel.id == plant_type_id)
        existing_plant_type.name = plant_type.name
        existing_plant_type.save()
        return {"message": "Plant type updated successfully"}
    except Exception as exc:  # Catch all exceptions
        raise HTTPException(status_code=404, detail="Plant type not found") from exc

# Delete Plant Type
@plant_route.delete("/plant-types/{plant_type_id}")
async def delete_plant_type(plant_type_id: int):
    """Delete a plant type from the database."""
    rows_deleted = PlantTypeModel.delete().where(PlantTypeModel.id == plant_type_id).execute()
    if rows_deleted:
        return {"message": "Plant type deleted successfully"}
    raise HTTPException(status_code=404, detail="Plant type not found")
