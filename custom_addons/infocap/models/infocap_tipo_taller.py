
from odoo import models, fields, api


class infocapTipoTaller(models.Model):
    _name = 'infocap.tipo.taller'
    _description = 'Registro de tipos taller'


    name=fields.Char('Tipo Taller')
    modalidad = fields.Selection([('individual', 'Individual'), ('grupal', 'Grupal')])
    duraccion = fields.Float('en horas') # duración total del taller

    documentos_ids = fields.One2many('infocap.documentos', 'tipo_taller_id', string='DOCUMENTACION TALLER')
    talleres_ids = fields.One2many('infocap.talleres', 'tipo_taller', string='TALLERES')
    



    