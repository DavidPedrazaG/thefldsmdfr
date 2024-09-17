from fastapi import APIRouter, Body, HTTPException
from schemas.plant_schema import Plant
from schemas.plant_type_schema import PlantType
from database import PlantModel, PlantTypeModel

plant_route = APIRouter()

# Create Plant
@plant_route.post("/")
async def create_plant(plant: Plant = Body(...)):
    PlantModel.create(
        name=plant.name,
        type=plant.type,
        description=plant.description
    )
    return {"message": "Plant created successfully"}

# Read All Plants
@plant_route.get("/")
async def read_all_plants():
    plants = PlantModel.select().dicts()
    return list(plants)

# Read Plant by ID
@plant_route.get("/{plant_id}")
async def read_plant(plant_id: int):
    try:
        plant = PlantModel.get(PlantModel.id == plant_id)
        return plant
    except PlantModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plant not found")

# Update Plant
@plant_route.put("/{plant_id}")
async def update_plant(plant_id: int, plant: Plant = Body(...)):
    try:
        existing_plant = PlantModel.get(PlantModel.id == plant_id)
        existing_plant.name = plant.name
        existing_plant.type = plant.type
        existing_plant.description = plant.description
        existing_plant.save()
        return {"message": "Plant updated successfully"}
    except PlantModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plant not found")

# Delete Plant
@plant_route.delete("/{plant_id}")
async def delete_plant(plant_id: int):
    rows_deleted = PlantModel.delete().where(PlantModel.id == plant_id).execute()
    if rows_deleted:
        return {"message": "Plant deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Plant not found")

# Create Plant Type
@plant_route.post("/plant-types/")
async def create_plant_type(plant_type: PlantType = Body(...)):
    PlantTypeModel.create(
        name=plant_type.name,
        description=plant_type.description
    )
    return {"message": "Plant type created successfully"}

# Read All Plant Types
@plant_route.get("/plant-types/")
async def read_all_plant_types():
    plant_types = PlantTypeModel.select().dicts()
    return list(plant_types)

# Read Plant Type by ID
@plant_route.get("/plant-types/{plant_type_id}")
async def read_plant_type(plant_type_id: int):
    try:
        plant_type = PlantTypeModel.get(PlantTypeModel.id == plant_type_id)
        return plant_type
    except PlantTypeModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plant type not found")

# Update Plant Type
@plant_route.put("/plant-types/{plant_type_id}")
async def update_plant_type(plant_type_id: int, plant_type: PlantType = Body(...)):
    try:
        existing_plant_type = PlantTypeModel.get(PlantTypeModel.id == plant_type_id)
        existing_plant_type.name = plant_type.name
        existing_plant_type.description = plant_type.description
        existing_plant_type.save()
        return {"message": "Plant type updated successfully"}
    except PlantTypeModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plant type not found")

# Delete Plant Type
@plant_route.delete("/plant-types/{plant_type_id}")
async def delete_plant_type(plant_type_id: int):
    rows_deleted = PlantTypeModel.delete().where(PlantTypeModel.id == plant_type_id).execute()
    if rows_deleted:
        return {"message": "Plant type deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Plant type not found")
