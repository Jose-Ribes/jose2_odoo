# Preparación para entorno de desarrollo

En primer lugar clonar repositorio base de ejemplo y después:

## Cambios en los fichero de configuración

Día 03-02-2026: He creado el módulo dronify_jose, dentro de este he creado dos modelos exactamente los modelos contactos_jose que hereda de rest.partner y el modelo drones_jose, he añadido el modelo de drones_jose en el archivo de seguridad pero no el de contactos_jose ya que este al heredar de rest_partner no me hace falta ponerlo, también he insertado en el archivo de views.xml la vista de formulario y de lista para el modelo de drones_jose para hacer una prueba y tambíen ya en odoo he creado un ejemplo de dron para comprobar que se podía crear correctamente.

Día 06-02-2026: He acabado la lógica de los modelos a falta de revisarlos para que me funcione además de insertar todos los modelos en el fichero de seguridad, en la siguiente sesión tengo que empezar a implementar las vistar e ir probando, además de cambiar algo del models.py si estuviera mal, me ha actualizado el módulo correctamente en el odoo.

Día 07-02-2026: He cambiado el models.py a falta de alguna cosa que tengo que modificar está prácticamente acabado, en las vistas tengo realizadas las vistas de drones y paquetes y la vista de lista de vuelos me falta hacer la vista de formulario de los vuelos y la vista completa de los contactos que tengo que preguntar varias cosas en clase.

Día 10-02-2026: He cambiado los errore que tenía en la vista tengo terminadas prácticamente la de paquetes, vuelos falta modificar alguna cosa, drones esta acabada y he empezado la de contactos empezando por la de pilotos y tengo casi acabada esta me faltaría acabar esta y empezar la de clientes.

Día 13-02-2026: He añadido la vista de formulario de pilotos rellenada correctamente, después también he añadido en el action de el views la vista de lista tanto de clientes como de pilotos y he eliminado el widget de percentage en las vistar de formulario y lista de vuelos, una vez hecho esto he puesto la funcionalidad de los botones en el models y luego en la vista con sus comprobaciones, he añadido comentarios en el models y views de la misma manera que los tenía en el rest_jose o en el gestión_tareas_jose, falta revisar fallos que tenga la aplicación revisar la funcionalidad de la aplicación y entenderla mejor, me falta también rellenar con datos coherentes la aplación.