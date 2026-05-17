from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .db import init_db, engine
from .api import blocks, reports, ws

app = FastAPI(title="Mentor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(blocks.router, prefix="/api/blocks", tags=["blocks"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(ws.router, prefix="/api/ws", tags=["ws"])

@app.get("/health")
def health():
    return {"status": "ok"}
