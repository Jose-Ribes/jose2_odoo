from odoo import models, fields, api


class gestion_restaurante_jose(models.Model):
     _name = 'gestion_restaurante_jose.platos_jose'
     _description = 'Modelo de Platos para Gestión de Restaurante'

     nombre = fields.Char()
#    value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
     descripcion = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

