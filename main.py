"""
Contract Intelligence AI - FastAPI Backend Entry Point
"""

import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.routes.upload import router as upload_router
from backend.routes.contracts import router as contracts_router
from backend.services.tracking import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    init_db()
    yield


app = FastAPI(
    title="Contract Intelligence AI",
    description="AI-powered legal contract analysis platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc),
            "path": str(request.url),
        },
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}"
    return response


app.include_router(upload_router, prefix="/api", tags=["Upload"])
app.include_router(contracts_router, prefix="/api", tags=["Contracts"])


@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "ok",
        "service": "Contract Intelligence AI",
        "version": "0.1.0",
    }


@app.get("/", tags=["System"])
async def root():
    return {
        "message": "Contract Intelligence AI API",
        "docs": "/docs",
        "health": "/health",
    }
