
from odoo import models, fields, api


class InfocapSectoresParticipantes(models.Model):
    _name = 'infocap.sectores.participantes'
    _description = 'Registro de Sectores de los participantes de infocap'


    participante_id=fields.Many2one('res.partner', string='participante')
    sectores_id=fields.Many2one('infocap.sectorocupacion', string='sector')