
from odoo import models, fields, api


class CaptacionTipoContratoss(models.Model):
    _name = 'captacion.tipo.contratoss'
    _description = 'Configuración Tipo Contrato SS'

    name = fields.Char(string='Clave')
    descripcion = fields.Char(string='Descripción')
    comentario = fields.Char(string='Comentario')
    estado = fields.Selection(string="Estado", default="activo",
                             selection=[('activo', 'Activo'),
                                        ('nodisponible', 'No Disponible')])

