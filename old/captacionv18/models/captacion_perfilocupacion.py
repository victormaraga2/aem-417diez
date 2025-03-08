
from odoo import models, fields, api


class CaptacionPerfilocupacion(models.Model):
    _name = 'captacion.perfilocupacion'
    _description = 'Registro de Perfil Ocupacion de captacion'


    name=fields.Char('Perfil Ocupación')
   