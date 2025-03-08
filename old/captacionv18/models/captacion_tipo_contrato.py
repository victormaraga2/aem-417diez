
from odoo import models, fields, api


class CaptacionTipoContrato(models.Model):
    _name = 'captacion.tipo.contrato'
    _description = 'Configuración Tipo Contrato'

    name = fields.Char(string='Tipo Contrato')
    estado = fields.Selection(string="Estado", default="activo",
                             selection=[('activo', 'Activo'),
                                        ('nodisponible', 'No Disponible')])

