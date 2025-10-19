from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from pathlib import Path

from .config.settings import settings
from .routers import text_transform

# Create upload directory
upload_dir = Path(settings.upload_dir)
upload_dir.mkdir(exist_ok=True)

app = FastAPI(
    title=settings.app_name,
    description="Text Studio API supporting text transformation, OCR, and multilingual translation",
    version="1.0.0",
    debug=settings.debug
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(text_transform.router)

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
