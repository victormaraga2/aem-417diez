
from odoo import models, fields, api


class InfocapSituacion(models.Model):
    _name = 'infocap.situacion'
    _description = 'Registro de Situacion del solicitante'


    name=fields.Char('Situación')