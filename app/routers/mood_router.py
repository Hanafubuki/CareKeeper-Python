from fastapi import APIRouter, Request
from datetime import date as date_datetime
from app.controllers.mood_controller import MoodTrackerController
from app.schemas.mood_schema import MoodSchema, MoodCreateSchema, MoodUpdateSchema


router = APIRouter(prefix="/mood", tags=["mood"])


@router.get("/{date}", response_model=MoodSchema)
async def get(date: date_datetime, request: Request):
    return await MoodTrackerController.get(date_=date, user_id=request.state.user.id)


@router.get("/", response_model=list[MoodSchema])
async def list_all(request: Request):
    return await MoodTrackerController.list_all(user_id=request.state.user.id)


@router.post("/")
async def create(data: MoodCreateSchema, request: Request):
    return await MoodTrackerController.create(user_id=request.state.user.id, data=data)


@router.put("/{date}")
async def update(data: MoodUpdateSchema, date: date_datetime, request: Request):
    return await MoodTrackerController.update(user_id=request.state.user.id, data=data, date_=date)


@router.delete("/{date}")
async def delete(date: date_datetime, request: Request):
    return await MoodTrackerController.delete(user_id=request.state.user.id, date_=date)
