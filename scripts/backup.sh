#!/bin/bash
# Script para crear un paquete de backup de datos desde Named Volume, subirlo a GitHub y reiniciar el entorno local.

echo "======================================================="
echo "    PASO 1: INICIANDO COPIA DE SEGURIDAD LOCAL"
echo "======================================================="

# Nombres según tu último docker-compose.yml
PG_CONTAINER="postgres_dev_jose"             # Nombre del contenedor de Postgres
ODOO_CONTAINER="odoo_dev_jose"               # Nombre del contenedor de Odoo
PG_USER="odoo"                              # Usuario de la BD Postgres
DB_NAME="odoo"                              # Nombre de la BD a respaldar 
BACKUP_DIR="./data/backups"                 # Directorio de backups en el host
BACKUP_SQL="${BACKUP_DIR}/${DB_NAME}.sql"   # Ruta completa del archivo SQL de backup

echo "==> Parando Odoo para garantizar consistencia..."
docker-compose stop "$ODOO_CONTAINER" 2>/dev/null || true

mkdir -p "${BACKUP_DIR}"

# Comprobar que el contenedor de Postgres está up
if ! docker ps --format '{{.Names}}' | grep -q "^${PG_CONTAINER}$"; then
  echo "==> Arrancando Postgres..."
  docker-compose up -d "$PG_CONTAINER"
fi


echo "==> Creando backup lógico (SQL plano) de la BD '${DB_NAME}'..."
# El dump se genera dentro del contenedor y se escribe en el bind mount /backups => ./data/backups del host
docker exec "${PG_CONTAINER}" bash -lc "pg_dump -U '${PG_USER}' -d '${DB_NAME}' > '/backups/${DB_NAME}.sql'"

# Opcional: sincronizar permisos en el host (por si el archivo queda con UID/GID del contenedor)
# sudo chmod 600 "${BACKUP_SQL}" || true

echo "Backup completado: ${BACKUP_SQL}"

echo "==> Arrancando Odoo de nuevo..."
docker compose start ${ODOO_CONTAINER}

exit

# 7. Añadir archivos al staging
echo "-> Añadiendo el nuevo paquete de datos y código a Git..."
sudo git add .

# 8. Realizar el commit
FECHA_BACKUP=$(date +"%Y-%m-%d %H:%M:%S")
echo "-> Creando commit..."
git commit -m "BACKUP AUTOMÁTICO - Datos (Volumen Nombrado) y código actualizados al $FECHA_BACKUP"

# 9. Subir a GitHub
echo "-> Subiendo a GitHub (rama main)..."

git push 

if [ $? -eq 0 ]; then
    echo "======================================================="
    echo " ¡ÉXITO! COPIA DE SEGURIDAD Y SUBIDA COMPLETADAS."
    echo "======================================================="
else
    echo "======================================================="
    echo " ERROR: FALLÓ LA SUBIDA A GITHUB."
    echo "======================================================="
fi