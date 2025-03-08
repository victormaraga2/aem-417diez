
from odoo import models, fields, api


class CaptacionAccionesParticipantes(models.Model):
    _name = 'captacion.acciones.participantes'
    _description = 'Registro de participantes por acción de captacion'


    participante_id=fields.Many2one('res.partner', string='participante')
    acciones_id=fields.Many2one('captacion.acciones.formativas', string='Acción')