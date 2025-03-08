
from odoo import models, fields, api


class GustoDatosAgrario(models.Model):
    _name = 'gusto.datos.agrario'
    _description = 'Registro de datos Agrario'
    _order = 'id'  # Orden por defecto basado en el campo ID


    concepto=fields.Char('Concepto')
    provincia=fields.Char('Provincia')
    real = fields.Integer('REAL')
    prev = fields.Integer('PREV', default=0)
    total = fields.Integer('TOTAL' , compute="_compute_total", store=True)

    @api.depends('real', 'prev')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.real + rec.prev




    