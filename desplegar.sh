#!/bin/bash

# Configuración de rutas
CLOUDFLARE_SCRIPT="npm/actualizar_ip_cloudflare.sh"
NPM_PATH="npm"
PROJECT_PATH="."

# Salir si ocurre cualquier error
set -e

echo "▶️  Actualizando IP en Cloudflare..."
chmod +x "$CLOUDFLARE_SCRIPT"
./"$CLOUDFLARE_SCRIPT"

echo "▶️  Levantando Nginx Proxy Manager..."
cd "$NPM_PATH"
docker-compose up -d
cd -

echo "▶️  Levantando Proyecto Django..."
cd "$PROJECT_PATH"
docker-compose up -d --build
cd -

echo "✅ Despliegue completado con éxito."
