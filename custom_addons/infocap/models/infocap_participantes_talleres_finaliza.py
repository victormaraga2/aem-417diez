from odoo import models, fields, api, _
from datetime import datetime, date, timedelta


class infocapParticipantesTalleresFinaliza(models.Model):

    #_inherit = 'mail.thread'
    _name = 'infocap.taller.participante'
    _description = 'Registro de Participantes en Talleres que finalizan'

    taller_id = fields.Many2one('infocap.talleres', string="Taller", required=True, ondelete='cascade')
    participante_id = fields.Many2one('res.partner', string="Participante", required=True, ondelete='cascade', domain="[('es_participante', '=', True)]")
    
    # Para partner
    finaliza = fields.Boolean(string="Finaliza Taller", default=False)


    