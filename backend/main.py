from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.services.reminder import start_scheduler, stop_scheduler

app = FastAPI(title="Experience Factory")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown():
    stop_scheduler()


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Register routers
from backend.routers import records, cards, coach
from backend.routers import settings as settings_router

app.include_router(records.router)
app.include_router(cards.router)
app.include_router(coach.router)
app.include_router(settings_router.router)
