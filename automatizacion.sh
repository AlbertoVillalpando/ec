#!/bin/bash

set -e  # Detener en cualquier error

# Variables de entorno
PROYECTO="easy-chair-uaz"
RUTA_PROYECTO="/root/admin/easy-chair-uaz"
BRANCH="main"
GIT_REPO="git@gitlab-ingsoftware.uaz.edu.mx:jrruiz68/easy-chair-uaz.git"
SERVICIO_WEB="easy-chair-uaz-web-1"
FECHA=$(date +%Y%m%d%H%M)
BACKUP_IMAGE="${PROYECTO}:backup-${FECHA}"

CLOUDFLARE_SCRIPT="$RUTA_PROYECTO/npm/actualizar_ip_cloudflare.sh"
NPM_PATH="$RUTA_PROYECTO/npm"
PROJECT_PATH="$RUTA_PROYECTO"

echo "▶️  Actualizando IP en Cloudflare..."
chmod +x "$CLOUDFLARE_SCRIPT"
"$CLOUDFLARE_SCRIPT"

echo "▶️  Levantando Nginx Proxy Manager..."
cd "$NPM_PATH"
docker-compose up -d
cd -

echo "📥 Haciendo pull del repositorio..."
cd "$PROJECT_PATH"
git reset --hard
git pull origin "$BRANCH"

echo "💾 Haciendo backup de la imagen actual..."
docker commit "$SERVICIO_WEB" "$BACKUP_IMAGE"

echo "🔨 Reconstruyendo y desplegando el proyecto..."
docker-compose down
docker-compose up -d --build

echo "🩺 Verificando estado del servicio..."
sleep 5
if curl -fs http://localhost:8000/ > /dev/null; then
    echo "✅ Despliegue exitoso"
else
    echo "❌ Error en despliegue. Restaurando versión anterior..."
    docker stop "$SERVICIO_WEB"
    docker rm "$SERVICIO_WEB"
    docker run -d --name "$SERVICIO_WEB" -p 8000:8000 "$BACKUP_IMAGE"
fi

echo "🎉 Automatización completada correctamente."
