# Mentor

AI-powered Digital Mentor & Schedule Manager — MVP scaffold.

Overview
- Breaks 24-hour day into short blocks (default 15 minutes).
- Tracks session progress in real-time (WebSocket) and via REST API.
- Generates automated insights/reports (OpenAI integration stub).

This branch contains a minimal full-stack scaffold (frontend + backend + docker-compose + CI) so you can run a local development environment and iterate.

Quick start (local, development):

1) Copy env variables:
   cp .env.example .env

2) Backend (local, without Docker):
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000

3) Frontend (local):
   cd frontend
   npm install
   npm run dev

4) Open http://localhost:3000 for the UI and http://localhost:8000/docs for FastAPI docs.

Notes
- The OpenAI integration is optional. Set OPENAI_API_KEY in .env to enable report generation.
- The backend uses a simple SQLModel/SQLite setup for quick dev. For production, point DATABASE_URL at Postgres and run migrations.

Structure
- backend/: FastAPI app
- frontend/: Next.js app (TypeScript)
- docker-compose.yml: example to run services together
- .github/workflows/ci.yml: basic CI
