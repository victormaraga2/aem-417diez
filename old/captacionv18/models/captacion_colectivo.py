
from odoo import models, fields, api


class CaptacionColectivo(models.Model):
    _name = 'captacion.colectivo'
    _description = 'Registro de Colectivos de captacion'

    
    name=fields.Char('Colectivo')