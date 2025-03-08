
from odoo import models, fields, api


class infocapTipoAccionformativa(models.Model):
    _name = 'infocap.tipo.accionformativa'
    _description = 'Registro de accion formativa sto'


    name=fields.Char('Acción Formativa')
    modalidad = fields.Selection([('presencial', 'Presencial'), ('online', 'Online')])
    duraccion = fields.Integer('en horas')


    documentos_ids = fields.One2many('infocap.documentos', 'tipo_accionformativa_id', string='DOCUMENTACION ACCION FORMATIVA')
    acciones_formativas_ids = fields.One2many('infocap.acciones.formativas', 'tipo_accionformativa_id', string='ACCIONES FORMATIVAS')
    # talleres_ids = fields.One2many('infocap.talleres', 'tipo_taller', string='TALLERES')



    

    