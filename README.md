# EntrenadorIA

**WhatsApp AI coaching assistant for personal trainers in Morelia, Michoacán.**

Built from Council deep session 2026-04-18 (`council-2026-04-18-b5c7`) — #1 pick (judge confidence 7.8, 28/36 votes).

## What it does
- Generates customized workout plans per client (goal / level / injuries) in ES or EN
- Analyzes exercise form from trainer descriptions
- Produces nutrition plans using affordable Mexican ingredients
- Suggests warm, motivating WhatsApp replies
- Tracks client progress (weight, BF%, adherence)
- Schedules training sessions

## Stack
- **CLI**: typer + rich
- **API**: FastAPI (19 endpoints)
- **Frontend**: React + TypeScript + Vite (7 pages, ES/EN)
- **AI**: Claude Haiku 4.5 (Anthropic SDK)
- **Storage**: JSON (`~/.entrenadoria/store.json`)
- **Deploy**: Frontend on Vercel, Backend on Render

## Quick start
```bash
pip install -e .
export ANTHROPIC_API_KEY=sk-ant-...
entrenadoria demo                  # seed demo data
entrenadoria clients list
entrenadoria workouts create <client_id> --duration 45 --language es
entrenadoria serve                 # http://localhost:8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev                        # http://localhost:5173
```

## CLI
```
entrenadoria clients add|list
entrenadoria workouts create|list
entrenadoria progress log|show
entrenadoria form analyze
entrenadoria nutrition plan
entrenadoria schedule list
entrenadoria whatsapp reply|thread
entrenadoria demo|status|serve
```

## Deploy
- Vercel (frontend): root = repo root, buildCommand from `vercel.json`
- Render (backend): connects to `render.yaml`, set `ANTHROPIC_API_KEY` env var
