#!/bin/bash
# Script final para restaurar datos directamente a un Volumen Nombrado de Docker.

echo "======================================================="
echo "    INICIANDO RESTAURACIÓN CON VOLUMEN NOMBRADO"
echo "======================================================="

PKG_PATH="data/backups/odoo_data_package.tar.gz"
VOLUME_NAME="odoo_dev_dam_postgres_data_volume" 
TEMP_DB_DIR="data/dataPostgreSQL" # Usamos la carpeta del Bind Mount como temporal
TEMP_ODOO_FIL=/tmp/odoo_filestore_temp # Usamos un temporal seguro para Odoo

# 1. Verificar si el paquete de datos existe
if [ ! -f $PKG_PATH ]; then
    echo "ERROR: No se encontró el archivo de datos '$PKG_PATH'. Asegúrate de haber hecho 'git pull'."
    exit 1
fi

# 2. Limpieza de volúmenes antiguos y directorios
echo "-> Eliminando volumen de PostgreSQL y carpetas locales antiguas..."
docker-compose down -v 
docker volume rm $VOLUME_NAME 2>/dev/null || true # Elimina el volumen nombrado para una restauración limpia
rm -rf $TEMP_DB_DIR data/odoo/filestore data/odoo/sessions 
mkdir -p $TEMP_DB_DIR # Recrea el directorio temporal

# 3. Desempaquetar los datos de PostgreSQL y Odoo en carpetas temporales
echo "-> Desempaquetando datos de PostgreSQL en $TEMP_DB_DIR..."
# Extrae solo el contenido de la base de datos a la carpeta temporal.
tar -xzvf $PKG_PATH -C $TEMP_DB_DIR --strip-components=1 data/dataPostgreSQL

# Extrae el filestore y sessions directamente a las carpetas Bind Mount (creará las carpetas)
echo "-> Restaurando filestore y sessions (Bind Mounts)..."
tar -xzvf $PKG_PATH 

# 4. Inyección de Datos en el Volumen Nombrado de PostgreSQL
# Copia los datos desde el directorio temporal del host al volumen gestionado por Docker
echo "-> Copiando datos de PostgreSQL (temp) al Volumen Nombrado..."
docker run --rm \
    -v $(pwd)/$TEMP_DB_DIR:/from_host \
    -v $VOLUME_NAME:/to_volume \
    postgres:15 \
    sh -c "cp -a /from_host/. /to_volume/ && chown -R postgres:postgres /to_volume/"

# 5. Limpieza del directorio temporal del host
echo "-> Limpiando directorio temporal..."
rm -rf $TEMP_DB_DIR

# 6. Levantar los servicios de Docker
echo "-> Iniciando Docker Compose..."
docker-compose up -d

echo "======================================================="
echo " ¡RESTAURACIÓN COMPLETA! Se ha corregido la lógica de inyección de datos."
echo " Acceso a Odoo en: http://localhost:8069"
echo "======================================================="