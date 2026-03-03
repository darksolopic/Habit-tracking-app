from pydantic import BaseModel, EmailStr
from datetime import date


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class HabitCreate(BaseModel):
    title: str
    description: str | None = None


class HabitResponse(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: date

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    total_habits: int
    completion_percentage: float
    current_streak: int