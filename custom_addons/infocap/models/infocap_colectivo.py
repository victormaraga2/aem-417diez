
from odoo import models, fields, api


class InfocapColectivo(models.Model):
    _name = 'infocap.colectivo'
    _description = 'Registro de Colectivos de infocap'

    
    name=fields.Char('Colectivo', required=True)