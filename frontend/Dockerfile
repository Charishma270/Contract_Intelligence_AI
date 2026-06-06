# ==============================================================================
# Contract Intelligence AI — Frontend Dockerfile
# ==============================================================================
# Day 23: Multi-stage build for React/Vite SPA.
#
#   Stage 1 (build)   — install deps + vite build → produces dist/
#   Stage 2 (serve)   — nginx serves static assets + proxies /api to backend
#
# Build:
#   docker build -t contract-ai-frontend ./frontend
#
# Run standalone:
#   docker run -p 5173:80 contract-ai-frontend
# ==============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Build — install dependencies and build static assets
# ---------------------------------------------------------------------------
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files first for layer caching
COPY package.json package-lock.json ./

# Install dependencies (clean install for reproducibility)
RUN npm ci

# Copy source code
COPY . .

# Build production bundle
RUN npm run build


# ---------------------------------------------------------------------------
# Stage 2: Serve — nginx with custom config
# ---------------------------------------------------------------------------
FROM nginx:alpine AS serve

# OCI metadata labels
LABEL org.opencontainers.image.title="Contract Intelligence AI Frontend" \
      org.opencontainers.image.description="React SPA for contract analysis — served via nginx with API reverse proxy" \
      org.opencontainers.image.version="0.6.0" \
      org.opencontainers.image.source="https://github.com/Charishma270/Contract_Intelligence_AI"

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

# Health check — verify nginx is serving
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
