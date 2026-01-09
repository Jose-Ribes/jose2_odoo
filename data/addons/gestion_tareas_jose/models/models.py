from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)

#TAREAS_JOSE ******************************************
#******************************************************
class tareas_jose(models.Model):
    _name = 'gestion_tareas_jose.tareas_jose'
    _description = 'gestion_tareas_jose.tareas_jose'

    name = fields.Char(
        string="Name", 
        required=True, 
        help="Introduzca el nombre de la tarea")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tarea")

    fecha_creacion = fields.Date(
        string="Fecha Creación", 
        required=True, 
        help="Fecha en la que se dio de alta la tarea")

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio de la tarea")

    fecha_fin = fields.Datetime(
        string="Fecha Final", 
        help="Fecha y hora de finalización de la tarea")

    finalizado = fields.Boolean(
        string="Finalizado", 
        help="Indica si la tarea ha sido finalizada o no")
    
    sprint = fields.Many2one(
        'gestion_tareas_jose.sprints_jose', 
        string='Sprint relacionado', 
        ondelete='set null', 
        help='Sprint al que pertenece esta tarea')
    
    # En el modelo tareas_sergio
    codigo = fields.Char(
        compute="_get_codigo",
        store=True)

    rel_tecnologias = fields.Many2many(
        comodel_name='gestion_tareas_jose.tecnologias_jose',
        relation='relacion_tareas_tecnologias',
        column1='rel_tareas',
        column2='rel_tecnologias',
        string='Tecnologías')
    
    #MÉTODOS --------------------------------------------
    #----------------------------------------------------
    @api.depends('sprint')
    def _get_codigo(self):
        _logger.info("Iniciando generación de códigos de tareas")

        for tarea in self:
            # Si no hay sprint o el registro aún no tiene ID, no generamos código.
            if not tarea.sprint:
                _logger.warning(f"Tarea {tarea.id} sin sprint asignado")
                tarea.codigo = False
                continue

            if not tarea.id:
                tarea.codigo = False
                continue

            try:
                tarea.codigo = f"{tarea.sprint.name}".upper() + "_" + str(tarea.id)
                _logger.debug(f"Código generado: {tarea.codigo}")
            except Exception as e:
                _logger.error(f"Error generando código para tarea {tarea.id}: {str(e)}")
                tarea.codigo = False

class sprints_jose(models.Model):
    _name = 'gestion_tareas_jose.sprints_jose'
    _description = 'gestion_tareas_jose.sprints_jose'
    _rec_name = 'nombre'

    nombre = fields.Char(
        string="Nombre Sprint", 
        required=True, 
        help="Introduzca el nombre del sprint")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción del sprint")

    fecha_ini = fields.Datetime(
        string="Fecha Inicio", 
        required=True, 
        help="Fecha y hora de inicio de la tarea")
    
    duracion = fields.Integer(
       string="Duración", 
        help="Cantidad de días que tiene asignado el sprint")

    fecha_fin = fields.Datetime(
        compute='_compute_fecha_fin',
        store=True,
        string="Fecha Final", 
        help="Fecha y hora de finalización de la tarea")
        
    tareas = fields.One2many(
        'gestion_tareas_jose.tareas_jose', 
        'sprint', 
        string='Tareas del Sprint')
    
    @api.depends('fecha_ini', 'duracion')
    def _compute_fecha_fin(self):
        try:
            for sprint in self:
                if sprint.fecha_ini and sprint.duracion and sprint.duracion >  -10:
                    sprint.fecha_fin = sprint.fecha_ini + timedelta(days=sprint.duracion)
                else:
                    sprint.fecha_fin = sprint.fecha_ini
        except Exception as e:
            raise ValidationError(f"Error al generar el código: {str(e)}")
        
    @api.constrains('fecha_ini', 'fecha_fin')
    def _check_fechas(self):
        for sprint in self:
            if sprint.fecha_fin and sprint.fecha_ini:
                if sprint.fecha_fin < sprint.fecha_ini:
                    raise ValidationError(
                        "La fecha de fin no puede ser anterior a la fecha de inicio."
                    )
    
class tecnologias_jose(models.Model):
    _name = 'gestion_tareas_jose.tecnologias_jose'
    _description = 'Modelo de Tecnologías'

    name = fields.Char(
        string="Nombre", 
        required=True, 
        help="Nombre de la tecnología")

    descripcion = fields.Text(
        string="Descripción", 
        help="Breve descripción de la tecnología")

    logo = fields.Image(
        string="Logo", 
        max_width=256, 
        max_height=256,
        help="Logo de la tecnología")
    
    rel_tareas = fields.Many2many(
        comodel_name='gestion_tareas_jose.tareas_jose',
        relation='relacion_tareas_tecnologias',
        column1='rel_tecnologias',
        column2='rel_tareas',
        string='Tareas')
