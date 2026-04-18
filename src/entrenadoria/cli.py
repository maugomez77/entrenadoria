"""EntrenadorIA CLI — typer + rich."""

from __future__ import annotations

from datetime import datetime

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import ai, demo, store

app = typer.Typer(help="WhatsApp AI coaching for personal trainers in Morelia.")
console = Console()

clients_app = typer.Typer(help="Client management.")
workouts_app = typer.Typer(help="Workout plans.")
progress_app = typer.Typer(help="Client progress tracking.")
form_app = typer.Typer(help="Exercise form analysis.")
nutrition_app = typer.Typer(help="Nutrition plans.")
schedule_app = typer.Typer(help="Appointments.")
wa_app = typer.Typer(help="WhatsApp messages.")

app.add_typer(clients_app, name="clients")
app.add_typer(workouts_app, name="workouts")
app.add_typer(progress_app, name="progress")
app.add_typer(form_app, name="form")
app.add_typer(nutrition_app, name="nutrition")
app.add_typer(schedule_app, name="schedule")
app.add_typer(wa_app, name="whatsapp")


# ---------- clients ----------

@clients_app.command("add")
def clients_add(name: str, phone: str, age: int,
                goal: str = "general_fitness", level: str = "beginner",
                injuries: str = "", notes: str = "") -> None:
    state = store.load()
    cli = {
        "id": store.new_id("cli"),
        "trainer_id": "trn_local",
        "name": name, "phone": phone, "age": age,
        "goal": goal, "level": level,
        "injuries": injuries, "notes": notes,
        "created_at": datetime.utcnow().isoformat(),
    }
    state["clients"].append(cli)
    store.save(state)
    console.print(f"[green]+[/green] Added client {name} ({cli['id']})")


@clients_app.command("list")
def clients_list() -> None:
    state = store.load()
    t = Table(title="Clientes / Clients")
    for col in ("ID", "Nombre", "Meta", "Nivel", "Lesiones"):
        t.add_column(col)
    for c in state["clients"]:
        t.add_row(c["id"], c["name"], c["goal"], c["level"], c.get("injuries") or "—")
    console.print(t)


# ---------- workouts ----------

@workouts_app.command("create")
def workouts_create(
    client_id: str,
    duration: int = 45,
    language: str = "es",
) -> None:
    state = store.load()
    cli = next((c for c in state["clients"] if c["id"] == client_id), None)
    if not cli:
        console.print("[red]Client not found[/red]"); raise typer.Exit(1)
    plan = ai.generate_workout_plan(cli["goal"], cli["level"], duration,
                                     cli.get("injuries", ""), language=language)  # type: ignore[arg-type]
    wk = {
        "id": store.new_id("wkt"),
        "client_id": client_id,
        "title": plan.get("title", ""),
        "focus": plan.get("focus", ""),
        "exercises": plan.get("exercises", []),
        "duration_minutes": duration,
        "language": language,
        "created_at": datetime.utcnow().isoformat(),
    }
    state["workouts"].append(wk)
    store.save(state)
    console.print(Panel.fit(
        f"[bold]{wk['title']}[/bold]\nFocus: {wk['focus']}\nDuration: {duration} min",
        title=f"Workout for {cli['name']}"))
    t = Table()
    for col in ("Exercise", "Sets", "Reps", "Rest"):
        t.add_column(col)
    for ex in wk["exercises"]:
        t.add_row(ex["name"], str(ex["sets"]), ex["reps"], f"{ex['rest_seconds']}s")
    console.print(t)


@workouts_app.command("list")
def workouts_list(client_id: str = "") -> None:
    state = store.load()
    rows = state["workouts"] if not client_id else [w for w in state["workouts"] if w["client_id"] == client_id]
    t = Table(title="Workouts")
    for col in ("ID", "Client", "Title", "Focus", "Duration"):
        t.add_column(col)
    names = {c["id"]: c["name"] for c in state["clients"]}
    for w in rows:
        t.add_row(w["id"], names.get(w["client_id"], "?"), w["title"], w["focus"], f"{w['duration_minutes']} min")
    console.print(t)


# ---------- progress ----------

@progress_app.command("log")
def progress_log(client_id: str, weight_kg: float = 0.0, body_fat_pct: float = 0.0,
                 adherence_score: float = 0.0, notes: str = "") -> None:
    state = store.load()
    p = {
        "id": store.new_id("prg"),
        "client_id": client_id,
        "date": datetime.utcnow().isoformat(),
        "weight_kg": weight_kg or None,
        "body_fat_pct": body_fat_pct or None,
        "adherence_score": adherence_score or None,
        "notes": notes,
    }
    state["progress"].append(p)
    store.save(state)
    console.print(f"[green]+[/green] Progress logged for {client_id}")


@progress_app.command("show")
def progress_show(client_id: str) -> None:
    state = store.load()
    entries = [p for p in state["progress"] if p["client_id"] == client_id]
    entries.sort(key=lambda p: p["date"])
    t = Table(title=f"Progress — {client_id}")
    for col in ("Date", "Weight (kg)", "BF %", "Adherence", "Notes"):
        t.add_column(col)
    for p in entries:
        t.add_row(p["date"][:10], str(p.get("weight_kg") or "—"),
                  str(p.get("body_fat_pct") or "—"),
                  str(p.get("adherence_score") or "—"),
                  p.get("notes") or "")
    console.print(t)


# ---------- form ----------

@form_app.command("analyze")
def form_analyze(client_id: str, exercise: str, description: str, language: str = "es") -> None:
    state = store.load()
    result = ai.analyze_exercise_form(exercise, description, language=language)  # type: ignore[arg-type]
    entry = {
        "id": store.new_id("fa"),
        "client_id": client_id,
        "exercise": exercise,
        "video_url": None,
        "issues": result.get("issues", []),
        "corrections": result.get("corrections", []),
        "score": result.get("score", 0),
        "language": language,
        "created_at": datetime.utcnow().isoformat(),
    }
    state["form_analyses"].append(entry)
    store.save(state)
    console.print(Panel.fit(
        f"[bold]{exercise}[/bold] — score {entry['score']}/10\n"
        f"Issues: {'; '.join(entry['issues'])}\n"
        f"Corrections: {'; '.join(entry['corrections'])}",
        title="Form analysis"))


# ---------- nutrition ----------

@nutrition_app.command("plan")
def nutrition_plan(client_id: str, weight_kg: float, activity_level: str = "moderate",
                   language: str = "es") -> None:
    state = store.load()
    cli = next((c for c in state["clients"] if c["id"] == client_id), None)
    if not cli:
        console.print("[red]Client not found[/red]"); raise typer.Exit(1)
    plan = ai.generate_nutrition_plan(cli["goal"], weight_kg, activity_level, language=language)  # type: ignore[arg-type]
    np_row = {
        "id": store.new_id("nut"),
        "client_id": client_id,
        "daily_calories": plan.get("daily_calories", 0),
        "protein_g": plan.get("protein_g", 0),
        "carbs_g": plan.get("carbs_g", 0),
        "fats_g": plan.get("fats_g", 0),
        "meal_ideas": plan.get("meal_ideas", []),
        "language": language,
        "created_at": datetime.utcnow().isoformat(),
    }
    state["nutrition_plans"].append(np_row)
    store.save(state)
    console.print(Panel.fit(
        f"Calories: {np_row['daily_calories']} kcal\n"
        f"P {np_row['protein_g']}g / C {np_row['carbs_g']}g / F {np_row['fats_g']}g\n"
        f"Meals:\n- " + "\n- ".join(np_row["meal_ideas"]),
        title=f"Nutrition — {cli['name']}"))


# ---------- schedule ----------

@schedule_app.command("list")
def schedule_list() -> None:
    state = store.load()
    t = Table(title="Upcoming sessions")
    for col in ("When", "Client", "Location", "Status"):
        t.add_column(col)
    names = {c["id"]: c["name"] for c in state["clients"]}
    for a in sorted(state["appointments"], key=lambda a: a["when"]):
        t.add_row(a["when"][:16], names.get(a["client_id"], "?"),
                  a.get("location", ""), a["status"])
    console.print(t)


# ---------- whatsapp ----------

@wa_app.command("reply")
def wa_reply(client_id: str, message: str, language: str = "es") -> None:
    state = store.load()
    cli = next((c for c in state["clients"] if c["id"] == client_id), None)
    if not cli:
        console.print("[red]Client not found[/red]"); raise typer.Exit(1)
    history_msgs = [m for m in state["messages"] if m["client_id"] == client_id][-6:]
    hist = "\n".join(f"{m['direction']}: {m['body']}" for m in history_msgs)
    suggestion = ai.suggest_whatsapp_reply(cli["name"], message, hist, language=language)  # type: ignore[arg-type]
    console.print(Panel.fit(suggestion, title=f"Suggested reply to {cli['name']}"))


@wa_app.command("thread")
def wa_thread(client_id: str) -> None:
    state = store.load()
    msgs = [m for m in state["messages"] if m["client_id"] == client_id]
    msgs.sort(key=lambda m: m["sent_at"])
    for m in msgs:
        prefix = "[cyan]>>[/cyan]" if m["direction"] == "in" else "[green]<<[/green]"
        console.print(f"{prefix} [{m['sent_at'][:16]}] {m['body']}")


# ---------- misc ----------

@app.command("demo")
def demo_cmd() -> None:
    """Seed realistic Morelia demo data."""
    demo.seed()
    console.print("[green]✓[/green] Demo data seeded")


@app.command("status")
def status() -> None:
    state = store.load()
    console.print(Panel.fit(
        f"Clients: {len(state['clients'])}\n"
        f"Workouts: {len(state['workouts'])}\n"
        f"Progress entries: {len(state['progress'])}\n"
        f"Form analyses: {len(state['form_analyses'])}\n"
        f"Nutrition plans: {len(state['nutrition_plans'])}\n"
        f"Appointments: {len(state['appointments'])}\n"
        f"Messages: {len(state['messages'])}",
        title="EntrenadorIA status"))


@app.command("serve")
def serve(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Run the FastAPI backend."""
    import uvicorn
    uvicorn.run("entrenadoria.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    app()
