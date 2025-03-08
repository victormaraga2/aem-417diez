
from odoo import models, fields, api


class CaptacionDocentesAcciones(models.Model):
    _name = 'captacion.docentes.acciones'
    _description = 'Registro de Docente en las acciones de captacion'


    docentes_id=fields.Many2one('captacion.docentes', string='docente')
    accion_id=fields.Many2one('captacion.acciones.formativas', string='Accion')