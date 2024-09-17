from fastapi import APIRouter, Body, HTTPException
from schemas.plant_schema import Plant
from schemas.plant_type_schema import PlantType
from database import PlantModel, PlantTypeModel

plant_route = APIRouter()

# Create Plant
@plant_route.post("/plants/")
async def create_plant(plant: Plant):
    new_plant = Plant(**plant.dict())
    await new_plant.save()
    return {"message": "Plant created successfully"}

# Read All Plants
@plant_route.get("/plants/")
async def read_all_plants():
    plants = await Plant.all()
    return [{"id": plant.id, "name": plant.name, "type": plant.type} for plant in plants]

# Read Plant by ID
@plant_route.get("/plants/{plant_id}")
async def read_plant(plant_id: int):
    plant = await Plant.get(plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return {"id": plant.id, "name": plant.name, "type": plant.type}

# Update Plant
@plant_route.put("/plants/{plant_id}")
async def update_plant(plant_id: int, plant: Plant):
    existing_plant = await Plant.get(plant_id)
    if existing_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    await existing_plant.update(**plant.dict())
    return {"message": "Plant updated successfully"}

# Delete Plant
@plant_route.delete("/plants/{plant_id}")
async def delete_plant(plant_id: int):
    plant = await Plant.get(plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    await plant.delete()
    return {"message": "Plant deleted successfully"}

# Create Plant Type
@plant_route.post("/plant-types/")
async def create_plant_type(plant_type: PlantType):
    new_plant_type = PlantType(**plant_type.dict())
    await new_plant_type.save()
    return {"message": "Plant type created successfully"}

# Read All Plant Types
@plant_route.get("/plant-types/")
async def read_all_plant_types():
    plant_types = await PlantType.all()
    return [{"id": plant_type.id, "name": plant_type.name} for plant_type in plant_types]

# Read Plant Type by ID
@plant_route.get("/plant-types/{plant_type_id}")
async def read_plant_type(plant_type_id: int):
    plant_type = await PlantType.get(plant_type_id)
    if plant_type is None:
        raise HTTPException(status_code=404, detail="Plant type not found")
    return {"id": plant_type.id, "name": plant_type.name}

# Update Plant Type
@plant_route.put("/plant-types/{plant_type_id}")
async def update_plant_type(plant_type_id: int, plant_type: PlantType):
    existing_plant_type = await PlantType.get(plant_type_id)
    if existing_plant_type is None:
        raise HTTPException(status_code=404, detail="Plant type not found")
    await existing_plant_type.update(**plant_type.dict())
    return {"message": "Plant type updated successfully"}

# Delete Plant Type
@plant_route.delete("/plant-types/{plant_type_id}")
async def delete_plant_type(plant_type_id: int):
    plant_type = await PlantType.get(plant_type_id)
    if plant_type is None:
        raise HTTPException(status_code=404, detail="Plant type not found")
    await plant_type.delete()
    return {"message": "Plant type deleted successfully"}