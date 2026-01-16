from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class rest_jose(models.Model):
    _name = 'rest_jose.rest_jose'
    _description = 'rest_jose.rest_jose'

    # CAMPOS ---------------------------------------------------------
    # ---------------------------------------------------------------
    
    value2 = fields.Float(compute="_value_pc", store=True)

    #@api.depends('value')
    #def _value_pc(self):
        #for record in self:
            #record.value2 = float(record.value) / 100

class platos_jose(models.Model):
    _name = 'rest_jose.platos_jose'
    _description = 'Modelo de Platos para Gestión de Restaurante'

    # CAMPOS ---------------------------------------------------------
    # ---------------------------------------------------------------
    
    name = fields.Char(
        string="Nombre", 
        required=False, 
        help="Nombre del Plato"
    )

    descripcion = fields.Text(
        string="Descripción", 
        required=False, 
        help="Descripción del Plato"
    )

    precio = fields.Float(
        string="Precio del Plato", 
        required=True, 
        help="Precio total de plato")
    
    descuento = fields.Float(
        string="Descuento (%)",
        default=0.0,
        help="Porcentaje de descuento aplicado al plato")
    
    # CAMPOS COMPUTADOS **********************************************
    # *****************************************************************
    
    codigo_plato = fields.Char(
        string="Código",
        compute="_get_codigo",
        help="Código automático del plato")
    
    precio_con_iva = fields.Float(
        string="Precio con IVA",
        compute="_compute_precio_con_iva",
        help="Precio con IVA incluido (10%)")
    
    precio_final = fields.Float(
        string="Precio Final",
        compute="_compute_precio_final",
        store=True,
        help="Precio final con descuento aplicado")
    
    tiempo_preparacion = fields.Integer(
        string="Tiempo Preparación", 
        required=False, 
        help="Tiempo de preparación del plato en minutos")
    
    disponible = fields.Boolean(
        string="Disponible", 
        default=True,
        required=False, 
        help="Disponibilidad del plato")
    
    categoria_id = fields.Many2one(
        comodel_name='rest_jose.categoria_jose',
        string='Categoría',
        help='Categoría a la que pertenece el plato'
    )

    # RELACIONES ****************************************************
    # *************************************************************** 

    chef_especializado = fields.Many2one(
        comodel_name='rest_jose.chef_jose',
        string='Chef especializado',
        compute='_compute_chef_especializado',
        store=True,
        help='Chef asignado automáticamente según la categoría del plato'
    )

    especialidad_chef = fields.Many2one(
        comodel_name='rest_jose.categoria_jose',
        related='chef_especializado.especialidad_id',
        string='Especialidad del chef',
        readonly=True,
        store=True,
        help='Categoría en la que se especializa el chef asignado'
    )
    
    menus = fields.Many2many(
        comodel_name='rest_jose.menu_jose',
        relation='rel_plato_menu',
        column1='plato_id',
        column2='menu_id',
        string='Menús',
        help='Menús en los que aparece este plato'
    )


    rel_ingredientes = fields.Many2many (
        comodel_name='rest_jose.ingrediente_jose',
        relation='relacion_platos_ingredientes',
        column1='rel_platos',
        column2='rel_ingredientes',
        string='Ingredientes')
    
    # ***************************************************************
    # MÉTODOS @api.depends (COMPUTADOS) ******************************

    @api.depends('categoria_id')
    def _compute_chef_especializado(self):
        """Asigna el primer chef cuya especialidad coincide con la categoría del plato."""
        Chef = self.env['rest_jose.chef_jose']
        for plato in self:
            if plato.categoria_id:
                plato.chef_especializado = Chef.search([
                    ('especialidad_id', '=', plato.categoria_id.id)
                ], limit=1)
            else:
                plato.chef_especializado = False
    
    @api.depends('categoria_id')
    def _get_codigo(self):
        for plato in self:
            try:
                if plato.id:
                    if not plato.categoria_id:
                        _logger.warning(f"El plato {plato.id} no tiene categoría asignada.")
                        plato.codigo_plato = f"PLT_{plato.id}"
                        _logger.debug(f"Código generado para plato sin categoría: {plato.codigo_plato}")
                    else:
                        nombre_categoria = plato.categoria_id.name or "CAT"
                        prefix = nombre_categoria[:3].upper()
                        plato.codigo_plato = f"{prefix}_{plato.id}"
                        _logger.debug(f"Código generado para plato {plato.id}: {plato.codigo_plato}")
                else:
                    plato.codigo_plato = "PLT_"
                    _logger.debug("Código temporal generado para plato sin ID")
            except Exception as e:
                _logger.error(f"Error al generar el código del plato: {str(e)}")
                raise ValidationError(f"Error al generar el código del plato: {str(e)}")
    
    def _compute_precio_con_iva(self):
        for plato in self:
            if plato.precio:
                plato.precio_con_iva = plato.precio * 1.10
            else:
                plato.precio_con_iva = 0.0
    
    @api.depends('precio', 'descuento')
    def _compute_precio_final(self):
        for plato in self:
            precio_base = plato.precio or 0.0
            descuento_decimal = (plato.descuento or 0.0) / 100.0
            plato.precio_final = precio_base * (1 - descuento_decimal)

    # MÉTODOS @api.constrains (VALIDACIONES) **************************
    # ***************************************************************
    
    @api.constrains('precio')
    def _verificar_precio(self):
        for plato in self:
            if plato.precio < 0:
                _logger.error(f"Precio inválido para plato {plato.id}: {plato.precio} (menor que 0)")
                raise ValidationError(f"El precio {plato.precio} no puede ser menor que 0")
            else:
                _logger.info(f"Precio validado correctamente para plato {plato.id}: {plato.precio}")

    @api.constrains('tiempo_preparacion')
    def _verificar_tiempoPreparacio(self):
        for plato in self:
            if plato.tiempo_preparacion:
                if plato.tiempo_preparacion < 1 or plato.tiempo_preparacion > 240:
                    _logger.error(f"Tiempo de preparación inválido para plato {plato.id}: {plato.tiempo_preparacion} minutos")
                    raise ValidationError(f"El tiempo de preparación debe estar entre un rango de 1 y 240 minutos.")
                else:
                    _logger.info(f"Tiempo de preparación validado para plato {plato.id}: {plato.tiempo_preparacion} minutos")
    
class menu_jose(models.Model):
    _name = 'rest_jose.menu_jose'
    _description = 'Modelo de Platos para Gestión de Restaurante'

    # CAMPOS ---------------------------------------------------------
    # ---------------------------------------------------------------
    
    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre del Menu"
    )

    descripcion = fields.Text(
        string="Descripción", 
        required=False, 
        help="Descripción del Menu"
    )

    fecha_inicio = fields.Date(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha Inicio del Menu"
    )

    fecha_fin = fields.Date(
        string="Fecha Fin", 
        required=False, 
        help="Fecha Fin del Menu"
    )

    activo = fields.Boolean(
        string="Activo", 
        required=False, 
        help="Comprobación de actividad del Menu"
    )

    # RELACIONES ****************************************************
    # ***************************************************************
    
    platos = fields.Many2many(
        comodel_name='rest_jose.platos_jose',
        relation='rel_plato_menu',
        column1='menu_id',
        column2='plato_id',
        string='Platos del Menu')

    categorias_platos = fields.Many2many(
        comodel_name='rest_jose.categoria_jose',
        string='Categorías de los platos',
        compute='_compute_categorias_platos',
        store=True,
        help='Categorías presentes en los platos de este menú'
    )
    
    # CAMPOS COMPUTADOS **********************************************
    # *****************************************************************
    
    precio_total = fields.Float(
        string="Precio Total del Menú",
        compute="_compute_precio_total",
        store=True,
        help="Suma total de los precios finales de todos los platos")

    @api.depends('platos', 'platos.categoria_id')
    def _compute_categorias_platos(self):
        for menu in self:
            menu.categorias_platos = menu.platos.mapped('categoria_id')
    
    # ***************************************************************
    # MÉTODOS @api.depends (COMPUTADOS) ******************************
    
    @api.depends('platos', 'platos.precio_final')
    def _compute_precio_total(self):
        for menu in self:
            menu.precio_total = sum(menu.platos.mapped('precio_final'))

    # MÉTODOS @api.constrains (VALIDACIONES) **************************
    # ***************************************************************
    
    @api.constrains('fecha_fin', 'fecha_inicio')
    def _comparar_fechas(self):
        for menu in self:
            if menu.fecha_fin:
                if menu.fecha_fin < menu.fecha_inicio:
                    raise ValidationError(f"La fecha fin debe ser posterior a la fecha de inicio.")
                
    @api.constrains('platos', 'activo')
    def _verificar_menus(self):
        for menu in self:
            if menu.activo:
                if len(menu.platos) < 1:
                    #_logger.warning(f"Intento de activar menú {menu.id} sin platos")
                    raise ValidationError(f"El menú {menu.name} está activo sin platos.")
    
class ingrediente_jose(models.Model):
    _name = 'rest_jose.ingrediente_jose'
    _description = 'Modelo de Ingredientes para Gestión de Restaurante'

    # CAMPOS ---------------------------------------------------------
    # ---------------------------------------------------------------
    
    name = fields.Char(
        string="Nombre", 
        required=False, 
        help="Nombre del Ingrediente"
    )

    es_alergeno = fields.Boolean (
        string="¿Es Alergeno?", 
        required=False, 
        help="Consulta si es alérgeno"
    )

    descripcion = fields.Text (
        string="Descripción", 
        required=False, 
        help="Descipción del Ingrediente"
    )

    # RELACIONES ****************************************************
    # ***************************************************************
    
    rel_platos = fields.Many2many (
        comodel_name='rest_jose.platos_jose',
        relation='relacion_platos_ingredientes',
        column1='rel_ingredientes',
        column2='rel_platos',
        string='Platos')
    
class categoria_jose(models.Model):
    _name = 'rest_jose.categoria_jose'
    _description = 'Modelo de Categorías para Gestión de Restaurante'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre de la Categoría"
    )

    descripcion = fields.Text(
        string="Descripción", 
        required=False, 
        help="Descripción de la Categoría"
    )

    platos_ids = fields.One2many(
        'rest_jose.platos_jose', 
        'categoria_id', 
        string='Platos de esta categoría')

    ingredientes_comunes = fields.Many2many(
        comodel_name='rest_jose.ingrediente_jose',
        string='Ingredientes comunes',
        compute='_compute_ingredientes_comunes',
        help='Ingredientes usados por cualquier plato de esta categoría'
    )

    @api.depends('platos_ids', 'platos_ids.rel_ingredientes')
    def _compute_ingredientes_comunes(self):
        Ingrediente = self.env['rest_jose.ingrediente_jose']
        for categoria in self:
            acumulado = Ingrediente
            for plato in categoria.platos_ids:
                acumulado = acumulado + plato.rel_ingredientes
            categoria.ingredientes_comunes = acumulado
    
class chef_jose(models.Model):
    _name = 'rest_jose.chef_jose'
    _description = 'Modelo de Chefs para Gestión de Restaurante'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre del Chef"
    )

    especialidad_id = fields.Many2one(
        comodel_name='rest_jose.categoria_jose',
        string='Categoría',
        help='Tipo de platos en los que es experto el chef'
    )

    platos_asignados = fields.One2many(
        'rest_jose.platos_jose', 
        'chef_especializado', 
        string='Platos asignados al chef')

