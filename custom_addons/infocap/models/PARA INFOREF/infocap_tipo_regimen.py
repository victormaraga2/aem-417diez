
from odoo import models, fields, api


class InfocapTipoRegimen(models.Model):
    _name = 'infocap.tipo.regimen'
    _description = 'Configuración Tipo regimen'

    name = fields.Char(string='Regimen')
    estado = fields.Selection(string="Estado", default="activo",
                             selection=[('activo', 'Activo'),
                                        ('nodisponible', 'No Disponible')])

