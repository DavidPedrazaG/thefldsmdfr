from fastapi import APIRouter, Body, HTTPException
from schemas.plant_schema import Plant
from schemas.plant_type_schema import PlantType
from database import PlantModel, PlantTypeModel

plant_route = APIRouter()

# Create Plant
@plant_route.post("/")
async def create_plant(plant: Plant = Body(...)):
    """Crea una nueva planta en la base de datos."""
    new_plant = PlantModel.create(
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
    """Obtiene una lista de todas las plantas."""
    plants = PlantModel.select().dicts()
    return list(plants)

# Read Plant by ID
@plant_route.get("/{plant_id}")
async def read_plant(plant_id: int):
    """Obtiene una planta específica por su ID."""
    try:
        plant = PlantModel.get(PlantModel.id == plant_id)
        return plant
    except PlantModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plant not found")

# Update Plant
@plant_route.put("/{plant_id}")
async def update_plant(plant_id: int, plant: Plant = Body(...)):
    """Actualiza la información de una planta existente."""
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
    except PlantModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plant not found")

# Delete Plant
@plant_route.delete("/{plant_id}")
async def delete_plant(plant_id: int):
    """Elimina una planta de la base de datos por su ID."""
    rows_deleted = PlantModel.delete().where(PlantModel.id == plant_id).execute()
    if rows_deleted:
        return {"message": "Plant deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Plant not found")

# Create Plant Type
@plant_route.post("/plant-types/")
async def create_plant_type(plant_type: PlantType = Body(...)):
    """Crea un nuevo tipo de planta."""
    PlantTypeModel.create(
        name=plant_type.name
    )
    return {"message": "Plant type created successfully"}

# Read All Plant Types
@plant_route.get("/plant-types/")
async def read_all_plant_types():
    """Obtiene una lista de todos los tipos de plantas."""
    plant_types = PlantTypeModel.select().dicts()
    return list(plant_types)

# Read Plant Type by ID
@plant_route.get("/plant-types/{plant_type_id}")
async def read_plant_type(plant_type_id: int):
    """Obtiene un tipo de planta específico por su ID."""
    try:
        plant_type = PlantTypeModel.get(PlantTypeModel.id == plant_type_id)
        return plant_type
    except PlantTypeModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plant type not found")

# Update Plant Type
@plant_route.put("/plant-types/{plant_type_id}")
async def update_plant_type(plant_type_id: int, plant_type: PlantType = Body(...)):
    """Actualiza la información de un tipo de planta existente."""
    try:
        existing_plant_type = PlantTypeModel.get(PlantTypeModel.id == plant_type_id)
        existing_plant_type.name = plant_type.name
        existing_plant_type.save()
        return {"message": "Plan Type updated successfully"}
    except PlantTypeModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="Plant type not found")

# Delete Plant Type
@plant_route.delete("/plant-types/{plant_type_id}")
async def delete_plant_type(plant_type_id: int):
    """Elimina un tipo de planta de la base de datos."""
    rows_deleted = PlantTypeModel.delete().where(PlantTypeModel.id == plant_type_id).execute()
    if rows_deleted:
        return {"message": "Plant type deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Plant type not found")
