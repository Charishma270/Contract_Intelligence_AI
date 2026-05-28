"""
Contract Intelligence AI — FastAPI Backend Entry Point
=====================================================
Main application with CORS, route registration,
global exception handling.

Day 12:
- Added /chat route
- Added /risk route
- Added RAG pipeline integration
- Added request-id middleware
- Added structured exception handling
Day 13: Integrated structured logging with file output,
        request-scoped context, and request/response logging.
"""

import os
import time
import uuid
import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from backend.routes.upload import (
    router as upload_router
)

from backend.routes.contracts import (
    router as contracts_router
)

from backend.routes.analyze import (
    router as analyze_router
)

from backend.routes.chat import (
    router as chat_router
)

from backend.routes.risk import (
    router as risk_router
)

from backend.routes.rag_routes import (
    router as rag_router
)

from backend.routes.frontend_analyze import (
    router as frontend_analyze_router
)

from backend.routes.async_analyze import (
    router as async_analyze_router
)

from backend.services.tracking import (
    init_db
)

from backend.utils.exceptions import (
    ContractAIError
)

from backend.utils.logging_config import (
    setup_logging,
    request_id_ctx,
)


logger = logging.getLogger("contract_ai")


# ---------------------------------------------------------
# Lifespan
# ---------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):

    """Initialize logging, DB, and directories on startup."""

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    os.makedirs(
        "data",
        exist_ok=True
    )

    os.makedirs(
        "logs",
        exist_ok=True
    )

    setup_logging()
    init_db()

    logger.info(
        "Contract Intelligence AI backend started"
    )

    yield

    logger.info(
        "Contract Intelligence AI backend shutting down"
    )


# ---------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------
app = FastAPI(

    title="Contract Intelligence AI",

    description=(
        "AI-powered legal contract "
        "analysis platform — OCR, NLP "
        "clause classification, semantic "
        "retrieval (RAG), and explainable "
        "risk scoring."
    ),

    version="0.5.0",

    lifespan=lifespan,
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ---------------------------------------------------------
# Exception Handlers
# ---------------------------------------------------------
@app.exception_handler(
    ContractAIError
)
async def contract_ai_exception_handler(
    request: Request,
    exc: ContractAIError
):

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "detail":
                exc.message,

            "error_type":
                type(exc).__name__,

            "path":
                str(request.url),
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):

    logger.error(

        f"Unhandled exception at "
        f"{request.url}: {exc}",

        exc_info=True
    )

    return JSONResponse(

        status_code=500,

        content={

            "detail":
                "Internal server error",

            "error_type":
                "InternalServerError",

            "path":
                str(request.url),
        },
    )


# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------
@app.middleware("http")
async def add_request_metadata(
    request: Request,
    call_next
):
    """Add request ID, process time, and structured request/response logging."""

    request_id = str(
        uuid.uuid4()
    )[:8]

    request_id_ctx.set(request_id)

    client_ip = request.client.host if request.client else "unknown"
    logger.info(
        f"\u2192 {request.method} {request.url.path} "
        f"(client={client_ip})"
    )

    start = time.perf_counter()

    response = await call_next(
        request
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    response.headers[
        "X-Process-Time"
    ] = f"{elapsed:.4f}"

    response.headers[
        "X-Request-ID"
    ] = request_id

    logger.info(
        f"\u2190 {request.method} {request.url.path} "
        f"status={response.status_code} time={elapsed:.4f}s"
    )

    return response


# ---------------------------------------------------------
# Register Routes
# ---------------------------------------------------------
app.include_router(

    upload_router,

    prefix="/api",

    tags=["Upload"]
)

app.include_router(

    contracts_router,

    prefix="/api",

    tags=["Contracts"]
)

app.include_router(

    analyze_router,

    prefix="/api",

    tags=["Analysis"]
)

app.include_router(

    chat_router,

    prefix="/api/chat",

    tags=["Chat"]
)

app.include_router(

    risk_router,

    prefix="/api/risk",

    tags=["Risk"]
)

app.include_router(

    rag_router,

    prefix="/api/rag",

    tags=["RAG Pipeline"]
)

# Async analysis (Day 17: Celery)
app.include_router(

    async_analyze_router,

    prefix="/api",

    tags=["Async Analysis"]
)

# Frontend integration — no /api prefix (Mukt's frontend calls POST /analyze)
app.include_router(

    frontend_analyze_router,

    tags=["Frontend Integration"]
)


# ---------------------------------------------------------
# Health Endpoint
# ---------------------------------------------------------
@app.get(
    "/health",
    tags=["System"]
)
async def health_check():

    return {

        "status":
            "ok",

        "service":
            "Contract Intelligence AI",

        "version":
            "0.5.0",
    }


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------
@app.get(
    "/",
    tags=["System"]
)
async def root():

    return {

        "message":
            "Contract Intelligence AI API",

        "docs":
            "/docs",

        "health":
            "/health",

        "endpoints": {

            "upload":
                "POST /api/upload",

            "contracts":
                "GET /api/contracts",

            "analyze":
                "POST /api/analyze/{contract_id}",

            "chat":
                "POST /api/chat",

            "risk":
                "GET /api/risk/{contract_id}",

            "rag_pipeline":
                "POST /api/rag/analyze",

            "async_analyze":
                "POST /api/analyze/{contract_id}/async",

            "task_status":
                "GET /api/tasks/{task_id}",
        },
    }