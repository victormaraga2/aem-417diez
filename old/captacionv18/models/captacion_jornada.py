
from odoo import models, fields, api


class CaptacionJornada(models.Model):
    _name = 'captacion.jornada'
    _description = 'Configuración de jornadas'

    name = fields.Char(string='Jornada Contrato', help="Jornada de contrato")
    pmc = fields.Char(string='Período Mínimo', help="Período mínimo Computable")
    estado = fields.Selection(string="Estado", default="activa",
                             selection=[('activa', 'Activa'),
                                        ('nodisponible', 'No Disponible')])
