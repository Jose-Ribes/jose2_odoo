from odoo import models, fields, api


class rest_jose(models.Model):
    _name = 'rest_jose.rest_jose'
    _description = 'rest_jose.rest_jose'
    
    value2 = fields.Float(compute="_value_pc", store=True)

    #@api.depends('value')
    #def _value_pc(self):
        #for record in self:
            #record.value2 = float(record.value) / 100

class platos_jose(models.Model):
    _name = 'rest_jose.platos_jose'
    _description = 'Modelo de Platos para Gestión de Restaurante'

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
    
    categoria = fields.Selection(
        [
            ('entrante', 'Entrante'),
            ('principal', 'Principal'),
            ('postre', 'Postre'),
            ('bebida', 'Bebida')
        ],
        string="Categoría", 
        required=False, 
        help="Categoría del Plato"
    )
    
    menu = fields.Many2one (
        'rest_jose.menu_jose',
        string='Menu relacionado con los platos',
        ondelete = 'set null',
        help='Menu al que pertenecen el plato o los platos'
    )


    rel_ingredientes = fields.Many2many (
        comodel_name='rest_jose.ingrediente_jose',
        relation='relacion_platos_ingredientes',
        column1='rel_platos',
        column2='rel_ingredientes',
        string='Ingredientes')
    
    @api.depends('categoria')
    def _get_codigo(self):
        for plato in self:
            if plato.id:
                if not plato.categoria:
                    plato.codigo_plato = f"PLT_{plato.id}"
                else:
                    prefix = plato.categoria[:3].upper()
                    plato.codigo_plato = f"{prefix}_{plato.id}"
            else:
                plato.codigo_plato = "PLT_"
    
    def _compute_precio_con_iva(self):
        for plato in self:
            if plato.precio:
                plato.precio_con_iva = plato.precio * 1.10
            else:
                plato.precio_con_iva = 0.0
    
    @api.depends('precio', 'descuento')
    def _compute_precio_final(self):
        for plato in self:
            descuento_aplicado = plato.precio * (plato.descuento / 100)
            plato.precio_final = plato.precio - descuento_aplicado
    
class menu_jose(models.Model):
    _name = 'rest_jose.menu_jose'
    _description = 'Modelo de Platos para Gestión de Restaurante'

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

    platos = fields.One2many(
        'rest_jose.platos_jose',
        'menu',
        string='Platos del Menu')
    
    precio_total = fields.Float(
        string="Precio Total del Menú",
        compute="_compute_precio_total",
        store=True,
        help="Suma total de los precios finales de todos los platos")
    
    @api.depends('platos', 'platos.precio_final')
    def _compute_precio_total(self):
        for menu in self:
            menu.precio_total = sum(menu.platos.mapped('precio_final'))
    
class ingrediente_jose(models.Model):
    _name = 'rest_jose.ingrediente_jose'
    _description = 'Modelo de Ingredientes para Gestión de Restaurante'

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

    rel_platos = fields.Many2many (
        comodel_name='rest_jose.platos_jose',
        relation='relacion_platos_ingredientes',
        column1='rel_ingredientes',
        column2='rel_platos',
        string='Platos')