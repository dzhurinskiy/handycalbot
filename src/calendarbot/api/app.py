"""FastAPI application setup."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from calendarbot.api.health import router as health_router
from calendarbot.api.oauth import router as oauth_router
from calendarbot.api.pages import router as pages_router
from calendarbot.config import get_settings

# Path to static files
STATIC_DIR = Path(__file__).parent.parent / "static"


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

    # Mount static files (for logo, favicon, robots.txt)
    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    # Include routers
    app.include_router(pages_router)  # Landing, privacy, terms pages
    app.include_router(health_router)
    app.include_router(oauth_router, prefix="/oauth")
    app.include_router(oauth_router, prefix="/auth")  # Also mount at /auth for Zoom

    return app
