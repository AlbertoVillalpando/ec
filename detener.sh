#!/bin/bash

echo "🛑 Deteniendo proyecto Django..."
cd "$(dirname "$0")"
docker-compose down

echo "🛑 Deteniendo Nginx Proxy Manager..."
cd npm
docker-compose down

echo "✅ Todos los servicios han sido detenidos correctamente."
