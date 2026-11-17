from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from database.connection import Database
from models.trainings import EnrollRequest, Training, TrainingUpdate

training_router = APIRouter(tags=["Trainings"])
training_database = Database(Training)

NOT_FOUND = "Training with supplied ID does not exist"


@training_router.get("/", response_model=List[Training])
async def retrieve_all_trainings() -> List[Training]:
    return await training_database.get_all()


# фильтр по тренеру -- объявлен ДО "/{id}", иначе "search" будет принят за id
@training_router.get("/search/by-trainer", response_model=List[Training])
async def find_by_trainer(trainer: str) -> List[Training]:
    return await Training.find(Training.trainer == trainer).to_list()


@training_router.get("/{id}", response_model=Training)
async def retrieve_training(id: PydanticObjectId) -> Training:
    training = await training_database.get(id)
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND)
    return training


@training_router.post("/new")
async def create_training(body: Training) -> dict:
    await training_database.save(body)
    return {"message": "Training created successfully"}


@training_router.put("/{id}", response_model=Training)
async def update_training(id: PydanticObjectId, body: TrainingUpdate) -> Training:
    updated = await training_database.update(id, body)
    if not updated:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND)
    return updated


@training_router.post("/{id}/enroll", response_model=Training)
async def enroll(id: PydanticObjectId, body: EnrollRequest) -> Training:
    """Запись клиента на занятие (используем оператор $push в MongoDB)."""
    training = await training_database.get(id)
    if not training:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND)
    if body.email in training.enrolled:
        raise HTTPException(status.HTTP_409_CONFLICT, "Client is already enrolled")
    if len(training.enrolled) >= training.capacity:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No free places")
    await training.update({"$push": {"enrolled": body.email}})
    return await training_database.get(id)


@training_router.delete("/{id}")
async def delete_training(id: PydanticObjectId) -> dict:
    if not await training_database.delete(id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, NOT_FOUND)
    return {"message": "Training deleted successfully."}
