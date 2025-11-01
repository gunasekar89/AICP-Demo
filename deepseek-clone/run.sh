#!/usr/bin/env bash
set -euo pipefail

# Determine project root (directory containing this script)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose.yml"

usage() {
  cat <<USAGE
Usage: $(basename "$0") [--build] [docker-compose args...]

Runs the DeepSeek clone stack (frontend, backend, worker, Redis, Postgres)
using Docker Compose. Additional arguments are forwarded to 'compose up'.

Options:
  --build       Rebuild images before starting (passes '--build' to compose).
  -h, --help    Show this help message.
USAGE
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
  usage
  exit 0
fi

# Determine docker compose command
if [[ -n "${DOCKER_COMPOSE_BIN:-}" ]]; then
  DOCKER_COMPOSE="$DOCKER_COMPOSE_BIN"
elif command -v docker-compose >/dev/null 2>&1; then
  DOCKER_COMPOSE="docker-compose"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  DOCKER_COMPOSE="docker compose"
else
  echo "Error: docker compose is required but was not found." >&2
  echo "Install Docker Desktop or docker-compose to continue." >&2
  exit 1
fi

# Ensure .env exists to avoid docker compose warnings
if [[ ! -f "$PROJECT_ROOT/.env" && -f "$PROJECT_ROOT/.env.example" ]]; then
  echo "Copying .env.example to .env (edit as needed)..."
  cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
fi

BUILD_FLAG=()
if [[ ${1:-} == "--build" ]]; then
  BUILD_FLAG=(--build)
  shift
fi

set -x
$DOCKER_COMPOSE -f "$COMPOSE_FILE" up "${BUILD_FLAG[@]}" "$@"
