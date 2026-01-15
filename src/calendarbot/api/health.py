"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {"service": "CalendarBot", "status": "running"}
