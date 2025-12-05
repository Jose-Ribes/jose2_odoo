from odoo import models, fields, api


class hola_mundo__v3(models.Model):
    _name = 'hola_mundo__v3.hola_mundo__v3'
    _description = 'hola_mundo__v3.hola_mundo__v3'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100

