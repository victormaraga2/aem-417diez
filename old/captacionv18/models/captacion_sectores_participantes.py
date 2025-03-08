
from odoo import models, fields, api


class CaptacionSectoresParticipantes(models.Model):
    _name = 'captacion.sectores.participantes'
    _description = 'Registro de Sectores de los participantes de captacion'


    participante_id=fields.Many2one('res.partner', string='participante')
    sectores_id=fields.Many2one('captacion.sectorocupacion', string='sector')