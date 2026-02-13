from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
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

# CONTACTOS (PILOTOS Y CLIENTES) *******************************
# **************************************************************
class contactos_jose(models.Model):
    _inherit = 'res.partner'

    # CAMPOS -------------------------------------------------------
    # --------------------------------------------------------------
    
    es_cliente = fields.Boolean(
        string="¿Es cliente?"
    )

    es_vip = fields.Boolean(
        string="Es vip" #Recordar repasar el modo ahorro de vuelos
    )

    es_piloto = fields.Boolean(
        string="¿Es piloto?"
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

# DRONES *******************************************************
# **************************************************************    
class drones_jose(models.Model):
    _name = 'dronify_jose.drones_jose'
    _description = 'dronify_jose.drones_jose'

    # CAMPOS -------------------------------------------------------
    # --------------------------------------------------------------
    
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
        help="Nivel de carga actual (0-100%)"
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

# PAQUETES *****************************************************
# **************************************************************    
class paquetes_jose(models.Model):
    _name = 'dronify_jose.paquetes_jose'
    _description = 'dronify_jose.paquetes_jose'

    # CAMPOS -------------------------------------------------------
    # --------------------------------------------------------------
    
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

# VUELOS *******************************************************
# **************************************************************
class vuelos_jose(models.Model):
    _name = 'dronify_jose.vuelos_jose'
    _description = 'dronify_jose.vuelos_jose'

    # CAMPOS -----------------------------------------------
    # --------------------------------------------------------------
    
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
    
    # RELACIONES ---------------------------------------------------
    # --------------------------------------------------------------

    paquetes_ids = fields.One2many(
        'dronify_jose.paquetes_jose', 
        'vuelo_id', 
        string='Paquetes a transportar')
    
    # CAMPOS ---------------------------------------------
    # --------------------------------------------------------------
    
    preparado = fields.Boolean(
        string="Preparado"
    )

    realizado = fields.Boolean(
        string="Realizado"
    )
    
    # CAMPOS COMPUTADOS ********************************************
    # **************************************************************

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
        """Suma automática del peso de todos los paquetes"""
        for vuelo in self:
            vuelo.peso_total = sum(vuelo.paquetes_ids.mapped('peso')) if vuelo.paquetes_ids else 0.0

    @api.depends('peso_total', 'dron_id', 'paquetes_ids.cliente_id.es_vip')
    def _compute_consumo_estimado(self):
        """Calcula consumo de batería verificando si hay clientes VIP"""
        for vuelo in self:
            # Obtener si algún cliente es VIP usando mapped()
            cliente_vip = False
            if vuelo.paquetes_ids:
                clientes = vuelo.paquetes_ids.mapped('cliente_id')
                cliente_vip = any(clientes.mapped('es_vip'))
            
            vuelo.consumo_estimado = calcular_consumo_vuelo(vuelo.peso_total, es_vip=cliente_vip)

    # MÉTODOS DE ACCIÓN (BOTONES) **********************************
    # **************************************************************

    def action_preparar_vuelo(self):
        """Prepara el vuelo y pone el dron en estado 'vuelo'"""
        for vuelo in self:
            vuelo.preparado = True
            if vuelo.dron_id:
                vuelo.dron_id.estado = 'vuelo'

    def action_desbloquear(self):
        """Desbloquea el vuelo para permitir edición"""
        for vuelo in self:
            if vuelo.realizado:
                raise UserError("No se puede desbloquear un vuelo que ya ha sido realizado.")
            vuelo.preparado = False

    def action_finalizar_vuelo(self):
        """Finaliza el vuelo, descuenta batería y libera el dron"""
        for vuelo in self:
            if not vuelo.preparado:
                raise UserError("El vuelo debe estar preparado antes de poder finalizarlo.")
            
            vuelo.realizado = True
            
            # Descontar el consumo estimado de la batería del dron
            if vuelo.dron_id:
                nueva_bateria = vuelo.dron_id.bateria - vuelo.consumo_estimado
                vuelo.dron_id.bateria = max(0, nueva_bateria)
                vuelo.dron_id.estado = 'disponible'

    # VALIDACIONES (CONSTRAINTS) ***********************************
    # **************************************************************

    @api.constrains('preparado', 'dron_id', 'piloto_id', 'paquetes_ids', 'peso_total')
    def _check_validaciones_preparacion(self):
        """Valida requisitos de seguridad antes de preparar un vuelo"""
        for vuelo in self:
            if vuelo.preparado:
                # 1. Asignaciones básicas
                if not vuelo.dron_id:
                    raise ValidationError("Debe asignar un dron antes de preparar el vuelo.")
                if not vuelo.piloto_id:
                    raise ValidationError("Debe asignar un piloto antes de preparar el vuelo.")
                
                # 2. Existencia de carga
                if not vuelo.paquetes_ids:
                    raise ValidationError("Debe asignar al menos un paquete antes de preparar el vuelo.")
                
                # 3. Capacidad de carga
                if vuelo.peso_total > vuelo.dron_id.capacidad_max:
                    raise ValidationError(
                        f"El peso total ({vuelo.peso_total} kg) supera la capacidad máxima del dron ({vuelo.dron_id.capacidad_max} kg)."
                    )
                
                # 4. Disponibilidad del dron
                if vuelo.dron_id.estado != 'disponible':
                    raise ValidationError(
                        f"El dron '{vuelo.dron_id.name}' no está disponible. Estado actual: {vuelo.dron_id.estado}"
                    )
                
                # 5. Batería suficiente
                if vuelo.dron_id.bateria < vuelo.consumo_estimado:
                    raise ValidationError(
                        f"Batería insuficiente. El dron tiene {vuelo.dron_id.bateria}% pero el vuelo requiere {vuelo.consumo_estimado}%."
                    )
                
                # 6. Certificación del piloto
                if vuelo.dron_id not in vuelo.piloto_id.dron_autorizado_ids:
                    raise ValidationError(
                        f"El piloto '{vuelo.piloto_id.name}' no está autorizado para pilotar el dron '{vuelo.dron_id.name}'."
                    )
