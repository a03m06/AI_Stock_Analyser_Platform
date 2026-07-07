from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routes
from app.routes.screener_routes import (
    router as screener_router
)

from app.routes.company_routes import (
    router as company_router
)

from app.routes.dashboard_routes import (
    router as dashboard_router
)


# ==================================================
# FastAPI App
# ==================================================

app = FastAPI(
    title="AI Stock Intelligence"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# Register Routes
# ==================================================

app.include_router(
    screener_router
)

app.include_router(
    company_router
)

app.include_router(
    dashboard_router
)


# ==================================================
# Root Endpoint
# ==================================================

@app.get("/")
def root():
    return {
        "message": "AI Stock Intelligence API Running"
    }