
from odoo import models, fields, api


class CaptacionSectorocupacion(models.Model):
    _name = 'captacion.sectorocupacion'
    _description = 'Registro de Sector ocupacion de captacion'


    name=fields.Char('Sector Ocupación')