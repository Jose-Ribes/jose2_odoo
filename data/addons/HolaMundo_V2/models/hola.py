# HolaMundo_V2/models/hola.py

from odoo import models, fields

class HolaMundo(models.Model):
    _name = 'hola.mundo.v2'
    _description = 'Modelo Hola Mundo V2'

    mensaje = fields.Char(string='Mensaje', default='¡Hola Mundo V2 desde Odoo!')