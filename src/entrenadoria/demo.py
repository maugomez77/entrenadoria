"""Seed realistic Morelia demo data."""

from datetime import datetime, timedelta

from . import store


TRAINER_ID = "trn_demo"

SEED_CLIENTS = [
    {"name": "Carlos Ramírez", "phone": "+524431234567", "age": 34,
     "goal": "weight_loss", "level": "beginner",
     "injuries": "molestia rodilla derecha", "notes": "Trabaja en oficina, tiempo limitado"},
    {"name": "Ana Gómez", "phone": "+524432345678", "age": 28,
     "goal": "muscle_gain", "level": "intermediate",
     "injuries": "", "notes": "Enfocada en fuerza de tren superior"},
    {"name": "Miguel Ángel Torres", "phone": "+524433456789", "age": 45,
     "goal": "rehabilitation", "level": "beginner",
     "injuries": "postoperatorio manguito rotador", "notes": "Refiere fisioterapeuta"},
    {"name": "Lucía Fernández", "phone": "+524434567890", "age": 22,
     "goal": "endurance", "level": "advanced",
     "injuries": "", "notes": "Entrena para maratón CDMX"},
    {"name": "Jorge Mendoza", "phone": "+524435678901", "age": 52,
     "goal": "general_fitness", "level": "beginner",
     "injuries": "hipertensión controlada", "notes": "Médico autorizó ejercicio moderado"},
]

SEED_WORKOUTS = [
    {"title": "Fuerza tren inferior", "focus": "piernas y glúteos",
     "duration_minutes": 45,
     "exercises": [
         {"name": "Sentadilla goblet", "sets": 3, "reps": "10-12", "rest_seconds": 90, "notes": "Mancuerna 8kg"},
         {"name": "Peso muerto rumano", "sets": 3, "reps": "10", "rest_seconds": 90, "notes": ""},
         {"name": "Zancadas caminando", "sets": 3, "reps": "12", "rest_seconds": 60, "notes": ""},
         {"name": "Puente de glúteo", "sets": 3, "reps": "15", "rest_seconds": 45, "notes": ""},
     ]},
    {"title": "Upper body hypertrophy", "focus": "chest and back",
     "duration_minutes": 55,
     "exercises": [
         {"name": "Bench press", "sets": 4, "reps": "8-10", "rest_seconds": 120, "notes": ""},
         {"name": "Bent-over row", "sets": 4, "reps": "8-10", "rest_seconds": 90, "notes": ""},
         {"name": "Overhead press", "sets": 3, "reps": "10", "rest_seconds": 90, "notes": ""},
         {"name": "Face pulls", "sets": 3, "reps": "15", "rest_seconds": 60, "notes": ""},
     ]},
]


def seed() -> dict:
    state = store.load()
    if state.get("clients"):
        return state

    for c in SEED_CLIENTS:
        cid = store.new_id("cli")
        state["clients"].append({
            "id": cid, "trainer_id": TRAINER_ID,
            "created_at": datetime.utcnow().isoformat(),
            **c,
        })

    for i, w in enumerate(SEED_WORKOUTS):
        if i >= len(state["clients"]):
            break
        state["workouts"].append({
            "id": store.new_id("wkt"),
            "client_id": state["clients"][i]["id"],
            "language": "es" if i == 0 else "en",
            "created_at": datetime.utcnow().isoformat(),
            **w,
        })

    # progress entries
    for cli in state["clients"][:3]:
        for days in (30, 20, 10, 0):
            state["progress"].append({
                "id": store.new_id("prg"),
                "client_id": cli["id"],
                "date": (datetime.utcnow() - timedelta(days=days)).isoformat(),
                "weight_kg": 78.0 - (30 - days) * 0.12,
                "body_fat_pct": 24.0 - (30 - days) * 0.08,
                "notes": "",
                "adherence_score": 7.5 + (30 - days) * 0.03,
            })

    # appointments for next week
    for i, cli in enumerate(state["clients"][:4]):
        state["appointments"].append({
            "id": store.new_id("apt"),
            "client_id": cli["id"],
            "trainer_id": TRAINER_ID,
            "when": (datetime.utcnow() + timedelta(days=i + 1, hours=17)).isoformat(),
            "duration_minutes": 60,
            "location": "Gimnasio Centro Morelia",
            "status": "scheduled",
        })

    # whatsapp thread
    for cli in state["clients"][:2]:
        state["messages"].extend([
            {"id": store.new_id("msg"), "client_id": cli["id"], "direction": "in",
             "body": "Hola, ¿puedo cambiar mi sesión del jueves?",
             "sent_at": (datetime.utcnow() - timedelta(hours=3)).isoformat()},
            {"id": store.new_id("msg"), "client_id": cli["id"], "direction": "out",
             "body": "¡Claro! ¿Viernes a la misma hora te acomoda?",
             "sent_at": (datetime.utcnow() - timedelta(hours=2, minutes=55)).isoformat()},
        ])

    store.save(state)
    return state
