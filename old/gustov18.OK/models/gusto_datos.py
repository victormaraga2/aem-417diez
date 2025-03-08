
from odoo import models, fields, api


class GustoDatos(models.Model):
    _name = 'gusto.datos'
    _description = 'Registro de datos'
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

    @api.model
    def action_actualizar_estadisticas_al_cargar(self):
        self.action_actualizar_estadisticas()
        return True

    def action_actualizar_estadisticas(self):
        gusto_records = self.env['gusto.gusto'].search([])  # Buscar todos los registros de gusto.gusto
        for record in gusto_records:
            record._compute_estadisticas()
            record._compute_fecha_objetivo()
            record._compute_sum_dias_computado()
        return True



    