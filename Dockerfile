# ==============================================================================
# Contract Intelligence AI — Backend Dockerfile
# ==============================================================================
# Day 22: Production-grade multi-stage build.
#
#   Stage 1 (builder)  — install Python dependencies into a venv
#   Stage 2 (runtime)  — slim image with only runtime deps + app code
#
# Build:
#   docker build -t contract-ai-backend .
#
# Run:
#   docker run -p 8000:8000 --env-file .env contract-ai-backend
# ==============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Builder — install Python packages
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# System deps needed to compile some Python packages (e.g. numpy, faiss-cpu)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment so we can copy it cleanly to the runtime stage
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies (layer cached — only re-runs when requirements change)
COPY requirements.docker.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.docker.txt


# ---------------------------------------------------------------------------
# Stage 2: Runtime — slim image with app code
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

# OCI metadata labels
LABEL org.opencontainers.image.title="Contract Intelligence AI Backend" \
      org.opencontainers.image.description="AI-powered legal contract analysis — OCR, NLP, RAG, risk scoring" \
      org.opencontainers.image.version="0.6.0" \
      org.opencontainers.image.authors="Team Backend <rushabh@contractai.dev>" \
      org.opencontainers.image.source="https://github.com/Charishma270/Contract_Intelligence_AI"

# Install runtime system dependencies:
#   - tesseract-ocr   → OCR fallback for scanned PDFs
#   - poppler-utils   → pdf2image (pdftoimage conversion)
#   - libgomp1        → OpenMP runtime for faiss-cpu
#   - curl            → health check probe
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        tesseract-ocr \
        poppler-utils \
        libgomp1 \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /app

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set production-appropriate environment defaults
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    LOG_LEVEL=INFO \
    HOST=0.0.0.0 \
    PORT=8000

# Copy application code
COPY . .

# Create writable directories and set ownership
RUN mkdir -p uploads data logs && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 8000

# Health check — polls /health every 30s, 5s timeout, 3 retries
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]