
from odoo import models, fields, api


class CaptacionPerfilesParticipantes(models.Model):
    _name = 'captacion.perfiles.participantes'
    _description = 'Registro de Perfiles de los participantes de captacion'


    participante_id=fields.Many2one('res.partner', string='participante')
    perfiles_id=fields.Many2one('captacion.perfilocupacion', string='perfil')