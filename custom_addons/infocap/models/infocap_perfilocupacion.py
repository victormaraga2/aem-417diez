
from odoo import models, fields, api


class InfocapPerfilocupacion(models.Model):
    _name = 'infocap.perfilocupacion'
    _description = 'Registro de Perfil Ocupacion de infocap'


    name=fields.Char('Perfil Ocupación')
   