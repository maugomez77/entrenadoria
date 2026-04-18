"""Anthropic Claude integrations for EntrenadorIA."""

from __future__ import annotations

import json
import os
from typing import Literal

from anthropic import Anthropic

MODEL = os.environ.get("ENTRENADORIA_MODEL", "claude-haiku-4-5-20251001")


def _client() -> Anthropic:
    return Anthropic()


def _ask_json(system: str, prompt: str, fallback: dict) -> dict:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return fallback
    try:
        resp = _client().messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0]
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0]
        return json.loads(text.strip())
    except Exception:
        return fallback


def generate_workout_plan(
    goal: str,
    level: str,
    duration_minutes: int,
    injuries: str,
    language: Literal["es", "en"] = "es",
) -> dict:
    lang_instr = "Responde en español mexicano neutro." if language == "es" else "Respond in English."
    system = (
        "You are an expert certified personal trainer designing safe, effective workouts "
        "for clients in Morelia, Michoacán. Adapt around listed injuries. " + lang_instr
    )
    prompt = (
        f"Goal: {goal}\nLevel: {level}\nDuration: {duration_minutes} minutes\n"
        f"Injuries/limitations: {injuries or 'none'}\n\n"
        "Return JSON: {\"title\": str, \"focus\": str, \"exercises\": "
        "[{\"name\": str, \"sets\": int, \"reps\": str, \"rest_seconds\": int, \"notes\": str}]}"
    )
    return _ask_json(system, prompt, {
        "title": "Full body basics" if language == "en" else "Rutina básica de cuerpo completo",
        "focus": "strength" if language == "en" else "fuerza",
        "exercises": [
            {"name": "Sentadilla" if language == "es" else "Squat",
             "sets": 3, "reps": "8-12", "rest_seconds": 90, "notes": ""},
            {"name": "Lagartija" if language == "es" else "Push-up",
             "sets": 3, "reps": "8-12", "rest_seconds": 60, "notes": ""},
            {"name": "Plancha" if language == "es" else "Plank",
             "sets": 3, "reps": "30s", "rest_seconds": 45, "notes": ""},
        ],
    })


def analyze_exercise_form(exercise: str, description: str, language: Literal["es", "en"] = "es") -> dict:
    lang_instr = "Responde en español." if language == "es" else "Respond in English."
    system = (
        "You are a biomechanics specialist. From a trainer's written description of a "
        "client's movement, infer likely form errors and corrections. " + lang_instr
    )
    prompt = (
        f"Exercise: {exercise}\nClient movement described: {description}\n\n"
        "Return JSON: {\"issues\": [str], \"corrections\": [str], \"score\": float 0-10}"
    )
    return _ask_json(system, prompt, {
        "issues": ["Rodillas colapsan hacia adentro"] if language == "es" else ["Knees cave inward"],
        "corrections": ["Empujar rodillas hacia afuera, alinear con dedos del pie"]
                        if language == "es"
                        else ["Push knees out, align with toes"],
        "score": 6.5,
    })


def generate_nutrition_plan(
    goal: str,
    weight_kg: float,
    activity_level: str,
    language: Literal["es", "en"] = "es",
) -> dict:
    lang_instr = "Responde en español mexicano." if language == "es" else "Respond in English."
    system = (
        "You are a sports nutrition expert designing plans using affordable Mexican ingredients "
        "(frijol, huevo, pollo, avena, tortilla integral, nopal, chía). " + lang_instr
    )
    prompt = (
        f"Goal: {goal}\nWeight: {weight_kg} kg\nActivity level: {activity_level}\n\n"
        "Return JSON: {\"daily_calories\": int, \"protein_g\": int, \"carbs_g\": int, "
        "\"fats_g\": int, \"meal_ideas\": [str x5]}"
    )
    return _ask_json(system, prompt, {
        "daily_calories": 2200,
        "protein_g": 150,
        "carbs_g": 220,
        "fats_g": 70,
        "meal_ideas": [
            "Huevo con nopales y frijoles",
            "Pechuga de pollo con arroz integral y brócoli",
            "Avena con plátano y chía",
            "Ensalada de atún con aguacate",
            "Tortilla integral con huevo y frijol",
        ] if language == "es" else [
            "Eggs with nopales and beans",
            "Grilled chicken with brown rice and broccoli",
            "Oatmeal with banana and chia",
            "Tuna salad with avocado",
            "Whole-grain tortilla with egg and beans",
        ],
    })


def suggest_whatsapp_reply(
    client_name: str,
    last_message: str,
    history: str = "",
    language: Literal["es", "en"] = "es",
) -> str:
    lang_instr = ("Responde como el entrenador personal en español mexicano, cálido y motivador."
                  if language == "es"
                  else "Reply as the personal trainer in warm, motivating English.")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return ("¡Listo! Cuéntame cómo te sientes y ajustamos el plan."
                if language == "es" else
                "Got it! Tell me how you're feeling and we'll adjust the plan.")
    try:
        resp = _client().messages.create(
            model=MODEL,
            max_tokens=400,
            system=lang_instr,
            messages=[{
                "role": "user",
                "content": (
                    f"Client: {client_name}\nRecent history:\n{history}\n\n"
                    f"Last message from client:\n{last_message}\n\n"
                    "Write a short, supportive reply (2-4 sentences)."
                ),
            }],
        )
        return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    except Exception:
        return ("¡Listo! Te veo pronto." if language == "es"
                else "Got it! See you soon.")
