#!/usr/bin/env bash
# ==============================================================================
# Contract Intelligence AI — AWS EC2 Deployment Script
# ==============================================================================
# Day 24: Automated provisioning and deployment for Ubuntu 22.04 EC2 instance.
#
# Usage:
#   chmod +x scripts/deploy.sh
#   ./scripts/deploy.sh              # Full deploy (idempotent)
#   ./scripts/deploy.sh --update     # Pull latest + restart services
#   ./scripts/deploy.sh --status     # Show container status only
#
# Prerequisites:
#   - EC2 instance: Ubuntu 22.04 LTS (t3.medium or larger)
#   - Security Groups: Inbound 22 (SSH), 80 (HTTP), 8000 (API), 6379 (Redis internal)
#   - A .env file with production secrets (see .env.production)
#
# Environment:
#   REPO_URL   — Git repository URL (default: https://github.com/Charishma270/Contract_Intelligence_AI)
#   APP_DIR    — Application directory on server (default: /opt/contract-ai)
#   GIT_BRANCH — Branch to deploy (default: main)
# ==============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_URL="${REPO_URL:-https://github.com/Charishma270/Contract_Intelligence_AI.git}"
APP_DIR="${APP_DIR:-/opt/contract-ai}"
GIT_BRANCH="${GIT_BRANCH:-main}"
COMPOSE_FILE="docker-compose.yml"
COMPOSE_PROD_FILE="docker-compose.prod.yml"
LOG_FILE="/var/log/contract-ai-deploy.log"

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'  # No Colour

log()  { echo -e "${GREEN}[DEPLOY]${NC} $*" | tee -a "$LOG_FILE"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $*" | tee -a "$LOG_FILE"; }
err()  { echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_FILE" >&2; }

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
MODE="full"
case "${1:-}" in
  --update) MODE="update" ;;
  --status) MODE="status" ;;
  --help|-h)
    echo "Usage: $0 [--update | --status | --help]"
    echo "  (no args)  Full deploy: install Docker, clone repo, start services"
    echo "  --update   Pull latest code and restart services"
    echo "  --status   Print current container status and exit"
    exit 0
    ;;
esac

# ---------------------------------------------------------------------------
# Status-only mode
# ---------------------------------------------------------------------------
if [[ "$MODE" == "status" ]]; then
  log "Service status:"
  cd "$APP_DIR"
  docker compose -f "$COMPOSE_FILE" -f "$COMPOSE_PROD_FILE" ps
  exit 0
fi

# ---------------------------------------------------------------------------
# Step 1 — System packages (full deploy only)
# ---------------------------------------------------------------------------
if [[ "$MODE" == "full" ]]; then
  log "Step 1/7 — Installing system dependencies..."
  sudo apt-get update -qq
  sudo apt-get install -y -qq \
    curl \
    git \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common

  # ---------------------------------------------------------------------------
  # Step 2 — Docker Engine
  # ---------------------------------------------------------------------------
  if ! command -v docker &>/dev/null; then
    log "Step 2/7 — Installing Docker Engine..."
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
      | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    echo "deb [arch=$(dpkg --print-architecture) \
      signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
      https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" \
      | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -qq
    sudo apt-get install -y -qq \
      docker-ce \
      docker-ce-cli \
      containerd.io \
      docker-compose-plugin

    sudo systemctl enable docker
    sudo systemctl start docker

    # Add current user to docker group (takes effect on next login)
    sudo usermod -aG docker "$USER" || true
    log "Docker installed. NOTE: Log out and back in for docker group to take effect."
  else
    log "Step 2/7 — Docker already installed ($(docker --version)). Skipping."
  fi

  # ---------------------------------------------------------------------------
  # Step 3 — Clone repository
  # ---------------------------------------------------------------------------
  if [[ ! -d "$APP_DIR/.git" ]]; then
    log "Step 3/7 — Cloning repository to $APP_DIR..."
    sudo mkdir -p "$APP_DIR"
    sudo chown "$USER":"$USER" "$APP_DIR"
    git clone --branch "$GIT_BRANCH" "$REPO_URL" "$APP_DIR"
  else
    log "Step 3/7 — Repository already cloned. Skipping."
  fi

  # ---------------------------------------------------------------------------
  # Step 4 — .env file check
  # ---------------------------------------------------------------------------
  log "Step 4/7 — Checking .env configuration..."
  if [[ ! -f "$APP_DIR/.env" ]]; then
    warn ".env not found at $APP_DIR/.env"
    warn "Copying .env.production template — you MUST edit it with real secrets!"
    cp "$APP_DIR/.env.production" "$APP_DIR/.env"
    warn "Edit $APP_DIR/.env now, then re-run this script with --update."
    exit 1
  fi
  log ".env file found."

  # ---------------------------------------------------------------------------
  # Step 5 — Create required directories
  # ---------------------------------------------------------------------------
  log "Step 5/7 — Creating runtime directories..."
  mkdir -p \
    "$APP_DIR/uploads" \
    "$APP_DIR/data" \
    "$APP_DIR/logs" \
    "$APP_DIR/data/vector_store"

  # ---------------------------------------------------------------------------
  # Step 6 — Pull & build images
  # ---------------------------------------------------------------------------
  log "Step 6/7 — Building Docker images..."
  cd "$APP_DIR"
  docker compose \
    -f "$COMPOSE_FILE" \
    -f "$COMPOSE_PROD_FILE" \
    build --no-cache

else
  # --update mode
  log "Step 1/3 — Pulling latest code from $GIT_BRANCH..."
  cd "$APP_DIR"
  git fetch origin
  git reset --hard "origin/$GIT_BRANCH"

  log "Step 2/3 — Rebuilding changed images..."
  docker compose \
    -f "$COMPOSE_FILE" \
    -f "$COMPOSE_PROD_FILE" \
    build
fi

# ---------------------------------------------------------------------------
# Final Step — Start services
# ---------------------------------------------------------------------------
log "Starting all services with production overrides..."
cd "$APP_DIR"
docker compose \
  -f "$COMPOSE_FILE" \
  -f "$COMPOSE_PROD_FILE" \
  up -d --remove-orphans

log "Waiting for health checks (30s)..."
sleep 30

log "Service status after deployment:"
docker compose \
  -f "$COMPOSE_FILE" \
  -f "$COMPOSE_PROD_FILE" \
  ps

log ""
log "================================================================"
log " Deployment complete!"
log " Backend API : http://\$(curl -s ifconfig.me):8000"
log " Frontend    : http://\$(curl -s ifconfig.me):5173"
log " API Docs    : http://\$(curl -s ifconfig.me):8000/docs"
log " Health      : http://\$(curl -s ifconfig.me):8000/health"
log "================================================================"
log "Run './scripts/healthcheck.sh' to verify all endpoints."
