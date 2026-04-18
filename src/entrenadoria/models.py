"""Pydantic models for EntrenadorIA."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Goal = Literal["weight_loss", "muscle_gain", "endurance", "rehabilitation", "general_fitness"]
Level = Literal["beginner", "intermediate", "advanced"]


class Client(BaseModel):
    id: str
    trainer_id: str
    name: str
    phone: str
    age: int
    goal: Goal
    level: Level
    injuries: str = ""
    notes: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Exercise(BaseModel):
    name: str
    sets: int
    reps: str  # "8-12" or "30s"
    rest_seconds: int
    notes: str = ""


class WorkoutPlan(BaseModel):
    id: str
    client_id: str
    title: str
    focus: str
    exercises: list[Exercise]
    duration_minutes: int
    language: Literal["es", "en"] = "es"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProgressEntry(BaseModel):
    id: str
    client_id: str
    date: datetime = Field(default_factory=datetime.utcnow)
    weight_kg: float | None = None
    body_fat_pct: float | None = None
    notes: str = ""
    adherence_score: float | None = None  # 0-10


class FormAnalysis(BaseModel):
    id: str
    client_id: str
    exercise: str
    video_url: str | None = None
    issues: list[str]
    corrections: list[str]
    score: float  # 0-10
    language: Literal["es", "en"] = "es"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class NutritionPlan(BaseModel):
    id: str
    client_id: str
    daily_calories: int
    protein_g: int
    carbs_g: int
    fats_g: int
    meal_ideas: list[str]
    language: Literal["es", "en"] = "es"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Appointment(BaseModel):
    id: str
    client_id: str
    trainer_id: str
    when: datetime
    duration_minutes: int = 60
    location: str = ""
    status: Literal["scheduled", "done", "cancelled", "no_show"] = "scheduled"


class WhatsAppMessage(BaseModel):
    id: str
    client_id: str
    direction: Literal["in", "out"]
    body: str
    sent_at: datetime = Field(default_factory=datetime.utcnow)
