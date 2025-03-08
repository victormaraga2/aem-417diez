
from odoo import models, fields, api


class InfocapSectorocupacion(models.Model):
    _name = 'infocap.sectorocupacion'
    _description = 'Registro de Sector ocupacion de infocap'


    name=fields.Char('Sector Ocupación')