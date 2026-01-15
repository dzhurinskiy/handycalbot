"""FastAPI application setup."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from calendarbot.api.health import router as health_router
from calendarbot.api.oauth import router as oauth_router
from calendarbot.config import get_settings


def create_app() -> FastAPI:
    """Create FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="CalendarBot API",
        description="OAuth callbacks and health checks for CalendarBot",
        version="0.1.0",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url=None,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if not settings.is_production else [],
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health_router)
    app.include_router(oauth_router, prefix="/oauth")

    return app
