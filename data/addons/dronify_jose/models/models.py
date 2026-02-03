from odoo import models, fields, api


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
        string="Identifica si el contacto es cliente"
    )

    es_vip = fields.Boolean(
        string="Marca clientes premium" #Recordar repasar el modo ahorro de vuelos
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
