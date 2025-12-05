# Preparación para entorno de desarrollo

En primer lugar clonar repositorio base de ejemplo y después:

## Cambios en los fichero de configuración

Una vez hecho el clonado **antes de restauar la base de datos** deben efectuarse cambios en los siguientes ficheros:

- `docker-compose.yml`: Cambiar todas las ocurencias de los nombre de los contenedores
  - por ejemplo, de `odoo_dev_dam` a `odoo_dev_sergio`
  - si se mantiene la raiz del nombre, solo reemplazar `dav` por `sergio`
- `data/odoo_config/odoo.conf`: 
  - En la línea 19, poner el mismo valor que en el fichero anterior en `postgres_dev_dam`
- `script/restore.sh` y `script/backup.sh`: actualizar las siguientes variables que se encuentran al principio de los scripts: 
  ```bash
  PG_CONTAINER="postgres_dev_dam"   # Nombre del contenedor de Postgres
  ODOO_CONTAINER="odoo_dev_dam"     # Nombre del contenedor de Odoo
  PG_USER="odoo"                    # Usuario de la BD Postgres
  DB_NAME="odoo"                    # Nombre de la BD a respaldar 
  ```

## Copia y restauración

Una vez se han hecho todos los cambios. 

### Para hacer copia

Para guardar los cambios

```bash
bash scripts/backup.sh

git add .                           # usar sudo si da errores de permisos
git commit -m "Comentario que sea"
git push
```

### para restaurar copia

```bash
git pull    # si te tienes que descargar desde tu repositorio la última versión.

bash scripts/restore.sh
```

## fichero `.gitignore`

Se debe preparar el fichero para no copiar en GitHub ficheros innecesarios que hagan la copia más pesada:

```bash
# ----------------------------------------------------------------
# IGNORAR TODOS LOS DATOS PERSISTENTES (¡MUY IMPORTANTE!)
# ----------------------------------------------------------------

# Ignorar los datos de la base de datos PostgreSQL
/data/dataPostgreSQL/

# Ignorar el filestore de Odoo (adjuntos, imágenes, etc.)
/data/odoo/filestore/

# Ignorar las sesiones de Odoo
/data/odoo/sessions/

# ----------------------------------------------------------------
# Archivos de sistema y Python
# ----------------------------------------------------------------

# Ignorar archivos compilados de Python
__pycache__/
*.pyc

# Ignorar archivos de sistema operativo
.DS_Store

# Ignorar carpetas de IDEs (opcional pero recomendado)
.vscode/
```