from datetime import datetime

from odoo import models, fields, api
from .logica_dronify import calcular_consumo_vuelo


class dronify_jose(models.Model):
    _name = 'dronify_jose.dronify_jose'
    _description = 'dronify_jose.dronify_jose'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

class contactos_jose(models.Model):
    _inherit = 'res.partner'

    es_cliente = fields.Boolean(
        string="Es cliente"
    )

    es_vip = fields.Boolean(
        string="Es vip" #Recordar repasar el modo ahorro de vuelos
    )

    es_piloto = fields.Boolean(
        string="Identifica si el contacto es piloto"
    )

    licencia = fields.Char(
        string="Licencia", 
        required=True, #Recordar cambiar que sea obligatorio solo para pilotos
        #El campo licencia debe ser obligatorio únicamente cuando es_piloto=True
        help="Número de licencia del piloto")
    
    dron_autorizado_ids = fields.Many2many(
        comodel_name="dronify_jose.drones_jose",
        relation='relacion_contactos_drones',
        column1='contacto_id',
        column2='dron_id',
        string="Drones autorizados")
    
class drones_jose(models.Model):
    _name = 'dronify_jose.drones_jose'
    _description = 'dronify_jose.drones_jose'

    name = fields.Char(
        string="Nombre", 
        help="Nombre identificativo del dron"
        )
    
    capacidad_max = fields.Float(
        string="Capacidad Máxima",
        required=True,
        help="Carga máxima en kilogramos"
    )

    bateria = fields.Integer(
        string="Batería del Dron",
        default=100,
        help="Nivel de carga actual (0-100%)	"
    )

    estado = fields.Selection(
        selection=[('disponible', 'Disponible'), ('vuelo', 'Vuelo'), ('taller', 'Taller')],
        default='disponible',
        string="Estado del Dron",
        help="Estado operativo del dron"
    )

    piloto_autorizado_ids = fields.Many2many(
        comodel_name="res.partner",
        relation='relacion_contactos_drones',
        column1='dron_id',
        column2='contacto_id',
        string="Pilotos certificados para este dron")
    
class paquetes_jose(models.Model):
    _name = 'dronify_jose.paquetes_jose'
    _description = 'dronify_jose.paquetes_jose'

    codigo = fields.Char(
        string="Código del Paquete",
        help="Identificador único",
        readonly=True,
        default=lambda self: datetime.now().strftime("%Y%m%d%H%M%S")
        )
    
    name = fields.Char(
        string="Descripción", 
        help="Descripción del contenido",
        required=True
        )
    
    peso = fields.Float(
        string="Peso (kg)",
        required=True,
        help="Peso en kilogramos"
    )

    cliente_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        domain=[('es_cliente', '=', True)]
    )

    vuelo_id = fields.Many2one(
        'dronify_jose.vuelos_jose',
        string='Vuelo asignado',
        readonly=True
    )

    dron_relacionado = fields.Char(
        related='vuelo_id.dron_id.name',
        string="Dron de Reparto",
        readonly=True,
        store=True
    )

class vuelos_jose(models.Model):
    _name = 'dronify_jose.vuelos_jose'
    _description = 'dronify_jose.vuelos_jose'

    codigo = fields.Char(
        string="Codigo",
        help="Código único del vuelo",
        readonly=True,
        default=lambda self: datetime.now().strftime("%Y%m%d%H%M%S")
        )
    
    name = fields.Char(
        string="Nombre", 
        help="Denominación de la misión",
        required=True,
        default=lambda self: datetime.now().strftime("%Y%m%d_Vuelo")
        )

    dron_id = fields.Many2one(
        'dronify_jose.drones_jose',
        string='Dron asignado',
        required=True
    )

    piloto_id = fields.Many2one(
        'res.partner',
        string='Piloto responsable',
        required=True,
        domain=[('es_piloto', '=', True)]
    )

    paquetes_ids = fields.One2many(
        'dronify_jose.paquetes_jose', 
        'vuelo_id', 
        string='Paquetes a transportar')
    
    preparado = fields.Boolean(
        string="Preparado"
    )

    realizado = fields.Boolean(
        string="Realizado"
    )

    peso_total = fields.Float(
        string="Peso Total",
        compute="_compute_peso_total",
        store=True,
        help="Suma del peso de todos los paquetes asignados"
    )

    consumo_estimado = fields.Float(
        string="Consumo Estimado",
        compute="_compute_consumo_estimado",
        store=True,
        help="Porcentaje de batería que consumirá el vuelo"
    )

    # MÉTODOS @api.depends (COMPUTADOS) ******************************
    # ***************************************************************

    @api.depends('paquetes_ids.peso')
    def _compute_peso_total(self):
        for vuelo in self:
            vuelo.peso_total = sum(vuelo.paquetes_ids.mapped('peso')) if vuelo.paquetes_ids else 0.0

    @api.depends('peso_total', 'dron_id')
    def _compute_consumo_estimado(self):
        for vuelo in self:
            # Obtener si el cliente es VIP
            cliente_vip = False
            if vuelo.paquetes_ids:
                cliente_vip = any(paquete.cliente_id.es_vip for paquete in vuelo.paquetes_ids)
            
            vuelo.consumo_estimado = calcular_consumo_vuelo(vuelo.peso_total, es_vip=cliente_vip)

    

