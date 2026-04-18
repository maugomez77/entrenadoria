"""FastAPI backend for EntrenadorIA."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import ai, demo, store

app = FastAPI(title="EntrenadorIA API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"],
)


# ---------- schemas ----------

class ClientIn(BaseModel):
    name: str
    phone: str
    age: int
    goal: str = "general_fitness"
    level: str = "beginner"
    injuries: str = ""
    notes: str = ""


class WorkoutRequest(BaseModel):
    client_id: str
    duration_minutes: int = 45
    language: Literal["es", "en"] = "es"


class FormRequest(BaseModel):
    client_id: str
    exercise: str
    description: str
    language: Literal["es", "en"] = "es"


class NutritionRequest(BaseModel):
    client_id: str
    weight_kg: float
    activity_level: str = "moderate"
    language: Literal["es", "en"] = "es"


class ReplyRequest(BaseModel):
    client_id: str
    last_message: str
    language: Literal["es", "en"] = "es"


class ProgressIn(BaseModel):
    client_id: str
    weight_kg: float | None = None
    body_fat_pct: float | None = None
    adherence_score: float | None = None
    notes: str = ""


class AppointmentIn(BaseModel):
    client_id: str
    when: datetime
    duration_minutes: int = 60
    location: str = ""


class MessageIn(BaseModel):
    client_id: str
    direction: Literal["in", "out"]
    body: str


# ---------- meta ----------

@app.get("/")
def root():
    return {
        "name": "EntrenadorIA API",
        "version": "0.1.0",
        "description": "WhatsApp AI coaching for personal trainers in Morelia",
        "endpoints": [
            "/clients", "/workouts", "/progress", "/form-analyses",
            "/nutrition-plans", "/appointments", "/messages",
            "/ai/workout", "/ai/form", "/ai/nutrition", "/ai/reply",
            "/status", "/demo/seed",
        ],
    }


@app.get("/status")
def status():
    state = store.load()
    return {k: len(v) for k, v in state.items()}


@app.post("/demo/seed")
def seed():
    demo.seed()
    return {"ok": True}


# ---------- clients ----------

@app.get("/clients")
def list_clients():
    return store.load()["clients"]


@app.post("/clients")
def create_client(c: ClientIn):
    state = store.load()
    rec = {
        "id": store.new_id("cli"),
        "trainer_id": "trn_default",
        "created_at": datetime.utcnow().isoformat(),
        **c.model_dump(),
    }
    state["clients"].append(rec)
    store.save(state)
    return rec


@app.get("/clients/{client_id}")
def get_client(client_id: str):
    state = store.load()
    cli = next((c for c in state["clients"] if c["id"] == client_id), None)
    if not cli:
        raise HTTPException(404, "client not found")
    return cli


# ---------- workouts ----------

@app.get("/workouts")
def list_workouts(client_id: str | None = None):
    wks = store.load()["workouts"]
    return [w for w in wks if not client_id or w["client_id"] == client_id]


@app.post("/ai/workout")
def ai_workout(req: WorkoutRequest):
    state = store.load()
    cli = next((c for c in state["clients"] if c["id"] == req.client_id), None)
    if not cli:
        raise HTTPException(404, "client not found")
    plan = ai.generate_workout_plan(cli["goal"], cli["level"], req.duration_minutes,
                                     cli.get("injuries", ""), language=req.language)
    wk = {
        "id": store.new_id("wkt"),
        "client_id": req.client_id,
        "title": plan.get("title", ""),
        "focus": plan.get("focus", ""),
        "exercises": plan.get("exercises", []),
        "duration_minutes": req.duration_minutes,
        "language": req.language,
        "created_at": datetime.utcnow().isoformat(),
    }
    state["workouts"].append(wk)
    store.save(state)
    return wk


# ---------- progress ----------

@app.get("/progress")
def list_progress(client_id: str | None = None):
    rows = store.load()["progress"]
    return [p for p in rows if not client_id or p["client_id"] == client_id]


@app.post("/progress")
def add_progress(p: ProgressIn):
    state = store.load()
    rec = {
        "id": store.new_id("prg"),
        "date": datetime.utcnow().isoformat(),
        **p.model_dump(),
    }
    state["progress"].append(rec)
    store.save(state)
    return rec


# ---------- form ----------

@app.post("/ai/form")
def ai_form(req: FormRequest):
    result = ai.analyze_exercise_form(req.exercise, req.description, language=req.language)
    state = store.load()
    rec = {
        "id": store.new_id("fa"),
        "client_id": req.client_id,
        "exercise": req.exercise,
        "video_url": None,
        "issues": result.get("issues", []),
        "corrections": result.get("corrections", []),
        "score": result.get("score", 0),
        "language": req.language,
        "created_at": datetime.utcnow().isoformat(),
    }
    state["form_analyses"].append(rec)
    store.save(state)
    return rec


@app.get("/form-analyses")
def list_form(client_id: str | None = None):
    rows = store.load()["form_analyses"]
    return [f for f in rows if not client_id or f["client_id"] == client_id]


# ---------- nutrition ----------

@app.post("/ai/nutrition")
def ai_nutrition(req: NutritionRequest):
    state = store.load()
    cli = next((c for c in state["clients"] if c["id"] == req.client_id), None)
    if not cli:
        raise HTTPException(404, "client not found")
    plan = ai.generate_nutrition_plan(cli["goal"], req.weight_kg, req.activity_level,
                                        language=req.language)
    rec = {
        "id": store.new_id("nut"),
        "client_id": req.client_id,
        "daily_calories": plan.get("daily_calories", 0),
        "protein_g": plan.get("protein_g", 0),
        "carbs_g": plan.get("carbs_g", 0),
        "fats_g": plan.get("fats_g", 0),
        "meal_ideas": plan.get("meal_ideas", []),
        "language": req.language,
        "created_at": datetime.utcnow().isoformat(),
    }
    state["nutrition_plans"].append(rec)
    store.save(state)
    return rec


@app.get("/nutrition-plans")
def list_nutrition(client_id: str | None = None):
    rows = store.load()["nutrition_plans"]
    return [n for n in rows if not client_id or n["client_id"] == client_id]


# ---------- appointments ----------

@app.get("/appointments")
def list_appointments():
    return store.load()["appointments"]


@app.post("/appointments")
def create_appointment(a: AppointmentIn):
    state = store.load()
    rec = {
        "id": store.new_id("apt"),
        "trainer_id": "trn_default",
        "status": "scheduled",
        **a.model_dump(),
    }
    rec["when"] = a.when.isoformat()
    state["appointments"].append(rec)
    store.save(state)
    return rec


# ---------- messages ----------

@app.get("/messages")
def list_messages(client_id: str | None = None):
    rows = store.load()["messages"]
    return [m for m in rows if not client_id or m["client_id"] == client_id]


@app.post("/messages")
def add_message(m: MessageIn):
    state = store.load()
    rec = {
        "id": store.new_id("msg"),
        "sent_at": datetime.utcnow().isoformat(),
        **m.model_dump(),
    }
    state["messages"].append(rec)
    store.save(state)
    return rec


@app.post("/ai/reply")
def ai_reply(req: ReplyRequest):
    state = store.load()
    cli = next((c for c in state["clients"] if c["id"] == req.client_id), None)
    if not cli:
        raise HTTPException(404, "client not found")
    history_msgs = [m for m in state["messages"] if m["client_id"] == req.client_id][-6:]
    hist = "\n".join(f"{m['direction']}: {m['body']}" for m in history_msgs)
    suggestion = ai.suggest_whatsapp_reply(cli["name"], req.last_message, hist,
                                             language=req.language)
    return {"suggestion": suggestion}
