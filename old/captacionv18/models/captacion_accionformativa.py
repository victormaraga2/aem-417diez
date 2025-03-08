
from odoo import models, fields, api


class CaptacionAccionfomativa(models.Model):
    _name = 'captacion.accionformativa'
    _description = 'Registro de accion formativa sto'


    name=fields.Char('Acción Formativa')
    duraccion = fields.Integer('en horas')

    