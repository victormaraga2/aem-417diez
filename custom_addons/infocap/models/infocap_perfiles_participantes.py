
from odoo import models, fields, api


class InfocapPerfilesParticipantes(models.Model):
    _name = 'infocap.perfiles.participantes'
    _description = 'Registro de Perfiles de los participantes de infocap'


    participante_id=fields.Many2one('res.partner', string='participante')
    perfiles_id=fields.Many2one('infocap.perfilocupacion', string='perfil')