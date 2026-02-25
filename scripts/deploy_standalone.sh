#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${PROJECT_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.yml}"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:8000/v1/health}"

cd "${PROJECT_DIR}"

echo "[deploy] Pulling latest images (if any)..."
docker compose -f "${COMPOSE_FILE}" pull || true

echo "[deploy] Building and starting services..."
docker compose -f "${COMPOSE_FILE}" up --build -d

echo "[deploy] Waiting for API health..."
for i in {1..30}; do
  if curl -sf "${HEALTH_URL}" >/dev/null; then
    echo "[deploy] Health check passed"
    exit 0
  fi
  sleep 2
done

echo "[deploy] Health check failed"
exit 1
