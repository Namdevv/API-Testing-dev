#!/bin/bash


# export COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME
export PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
export COMPOSE_PROJECT_NAME=$(basename "$PROJECT_ROOT")

echo "Project root: $PROJECT_ROOT"
echo "Compose project name: $COMPOSE_PROJECT_NAME"

# load env file and export variables if it exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

# --- Thêm: kiểm tra và tạo docker network "gateway_net" nếu chưa tồn tại ---
if ! docker network inspect gateway_net >/dev/null 2>&1; then
    echo "Docker network 'gateway_net' not found. Creating..."
    docker network create gateway_net
fi
# --- kết thúc thêm ---
# --- Thêm: kiểm tra và tạo docker network "cloudflare_tunnel_net" nếu chưa tồn tại ---
if ! docker network inspect cloudflare_tunnel_net >/dev/null 2>&1; then
    echo "Docker network 'cloudflare_tunnel_net' not found. Creating..."
    docker network create cloudflare_tunnel_net
fi
# --- kết thúc thêm ---


# Xác định file compose
COMPOSE_FILE="$PROJECT_ROOT/deploy/compose/docker-compose.yml"
OVERRIDE_FILE="$PROJECT_ROOT/deploy/compose/docker-compose.override.yml"

# Xử lý tag dev khi chạy
TAG="$1"

if [ "$TAG" == "dev" ] && [ -f "$OVERRIDE_FILE" ]; then
    export ENVIRONMENT="dev"

    echo "Run server (dev)"
    docker compose -f "$COMPOSE_FILE" -f "$OVERRIDE_FILE" --project-directory "$PROJECT_ROOT" up -d
elif [ "$TAG" == "stop" ]; then
    echo "Stop server"
    docker compose -f "$COMPOSE_FILE" --project-directory "$PROJECT_ROOT" down
else
    echo "Run server"
    docker compose -f "$COMPOSE_FILE" --project-directory "$PROJECT_ROOT" up -d
fi