#!/bin/bash
# Script para crear un paquete de backup de datos desde Named Volume, subirlo a GitHub y reiniciar el entorno local.

echo "======================================================="
echo "    PASO 1: INICIANDO COPIA DE SEGURIDAD LOCAL"
echo "======================================================="

PKG_PATH="data/backups/odoo_data_package.tar.gz"
TEMP_DB_DIR="data/temp_postgres_dump"
VOLUME_NAME="odoo_dev_dam_postgres_data_volume" # Nombre del volumen de Docker

# 1. Detener los servicios para garantizar la integridad de los datos
echo "-> Deteniendo contenedores..."
docker-compose stop

# 2. Preparación de directorios
rm -f $PKG_PATH
rm -rf $TEMP_DB_DIR
mkdir -p $TEMP_DB_DIR

# 3. EXTRAER DATOS DEL VOLUMEN NOMBRADO
echo "-> Copiando datos de PostgreSQL desde el Volumen Nombrado a directorio temporal..."
docker run --rm \
    -v $VOLUME_NAME:/from_volume \
    -v $(pwd)/$TEMP_DB_DIR:/to_host \
    postgres:15 \
    sh -c "cp -a /from_volume/. /to_host/"

# 4. Empaquetar: DB (temporal), Filestore y Sessions (Bind Mounts)
echo "-> Empaquetando datos (Named Volume + Bind Mounts) en $PKG_PATH..."
tar -czvf $PKG_PATH \
    $TEMP_DB_DIR \
    data/odoo/filestore \
    data/odoo/sessions \
    --transform 's|data/temp_postgres_dump|data/dataPostgreSQL|'

# 5. Limpiar directorios temporales
echo "-> Limpiando directorio temporal..."
rm -rf $TEMP_DB_DIR

# 6. Iniciar los contenedores inmediatamente para continuar el trabajo
echo "-> Iniciando contenedores de nuevo para continuar el trabajo..."
docker-compose start

echo "✅ Copia de seguridad local completada y entorno reiniciado."
echo "falta subit a GitHub..."

exit


echo "======================================================="
echo "    PASO 2: SUBIENDO CAMBIOS A GITHUB"
echo "======================================================="

# 7. Añadir archivos al staging
echo "-> Añadiendo el nuevo paquete de datos y código a Git..."
git add $PKG_PATH .

# 8. Realizar el commit
FECHA_BACKUP=$(date +"%Y-%m-%d %H:%M:%S")
echo "-> Creando commit..."
git commit -m "BACKUP AUTOMÁTICO - Datos (Volumen Nombrado) y código actualizados al $FECHA_BACKUP"

# 9. Subir a GitHub
echo "-> Subiendo a GitHub (rama main)..."
exit

git push origin main

if [ $? -eq 0 ]; then
    echo "======================================================="
    echo " ¡ÉXITO! COPIA DE SEGURIDAD Y SUBIDA COMPLETADAS."
    echo "======================================================="
else
    echo "======================================================="
    echo " ERROR: FALLÓ LA SUBIDA A GITHUB."
    echo "======================================================="
fi