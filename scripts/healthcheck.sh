#!/usr/bin/env bash
# ==============================================================================
# Contract Intelligence AI — Post-Deploy Health Check
# ==============================================================================
# Day 24: Smoke-tests all major API endpoints after a deployment.
#
# Usage:
#   chmod +x scripts/healthcheck.sh
#   ./scripts/healthcheck.sh                         # Check localhost:8000
#   BASE_URL=http://1.2.3.4:8000 ./scripts/healthcheck.sh
#
# Exit codes:
#   0 — All checks passed
#   1 — One or more checks failed
# ==============================================================================

set -uo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
TIMEOUT=10
PASS=0
FAIL=0

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}✓${NC} $*"; ((PASS++)); }
fail() { echo -e "  ${RED}✗${NC} $*"; ((FAIL++)); }
info() { echo -e "${YELLOW}►${NC} $*"; }

# ---------------------------------------------------------------------------
# Helper: HTTP GET check
#   check_get <label> <path> <expected_status>
# ---------------------------------------------------------------------------
check_get() {
  local label="$1"
  local path="$2"
  local expected="${3:-200}"

  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    --max-time "$TIMEOUT" \
    "${BASE_URL}${path}" 2>/dev/null) || status="CONN_ERR"

  if [[ "$status" == "$expected" ]]; then
    ok "$label → HTTP $status"
  else
    fail "$label → expected HTTP $expected, got $status"
  fi
}

# ---------------------------------------------------------------------------
# Helper: Check JSON field in response
#   check_json_field <label> <path> <jq_filter> <expected_value>
# ---------------------------------------------------------------------------
check_json_field() {
  local label="$1"
  local path="$2"
  local jq_filter="$3"
  local expected="$4"

  if ! command -v jq &>/dev/null; then
    info "jq not installed — skipping JSON field check for $label"
    return
  fi

  local actual
  actual=$(curl -s --max-time "$TIMEOUT" "${BASE_URL}${path}" \
    | jq -r "$jq_filter" 2>/dev/null) || actual="PARSE_ERR"

  if [[ "$actual" == "$expected" ]]; then
    ok "$label → $jq_filter == \"$expected\""
  else
    fail "$label → $jq_filter expected \"$expected\", got \"$actual\""
  fi
}

# ===========================================================================
echo ""
echo "============================================================"
echo "  Contract Intelligence AI — Health Check"
echo "  Target: $BASE_URL"
echo "  Time:   $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo ""

# ---------------------------------------------------------------------------
# 1. System endpoints
# ---------------------------------------------------------------------------
info "System Endpoints"
check_get      "GET /health"          "/health"          200
check_json_field "  status field"     "/health"          ".status"  "ok"
check_get      "GET /"                "/"                200

# ---------------------------------------------------------------------------
# 2. Contract management
# ---------------------------------------------------------------------------
info "Contract Endpoints"
check_get      "GET /api/contracts"           "/api/contracts"           200
check_get      "GET /api/contracts (page=1)"  "/api/contracts?page=1"    200
check_get      "GET /api/contracts (unknown)" "/api/contracts/nonexistent-id-9999" 404

# ---------------------------------------------------------------------------
# 3. Vector DB
# ---------------------------------------------------------------------------
info "Vector DB Endpoints"
check_get      "GET /api/vectordb/status"  "/api/vectordb/status"  200
check_get      "GET /api/vectordb/chunks"  "/api/vectordb/chunks"  200

# ---------------------------------------------------------------------------
# 4. API docs
# ---------------------------------------------------------------------------
info "API Documentation"
check_get      "GET /docs"    "/docs"    200
check_get      "GET /openapi.json" "/openapi.json" 200

# ---------------------------------------------------------------------------
# 5. Summary
# ---------------------------------------------------------------------------
echo ""
echo "============================================================"
echo -e "  Results: ${GREEN}${PASS} passed${NC}  ${RED}${FAIL} failed${NC}"
echo "============================================================"
echo ""

if [[ "$FAIL" -gt 0 ]]; then
  echo -e "${RED}Health check FAILED — see failures above.${NC}"
  exit 1
else
  echo -e "${GREEN}All health checks passed!${NC}"
  exit 0
fi
