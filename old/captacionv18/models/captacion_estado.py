
from odoo import models, fields, api


class CaptacionTaller(models.Model):
    _name = 'captacion.taller'
    _description = 'Registro de taller'


    name=fields.Char('Taller')
    modalidad = fields.Selection([('individual', 'Individual'), ('grupal', 'Grupal')])
    duraccion = fields.Integer('en horas')


    