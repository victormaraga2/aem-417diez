
from odoo import models, fields, api


class infocapDocumentos(models.Model):
    _name = 'infocap.documentos'
    _description = 'Registro de documentos'


    participante_id = fields.Many2one('res.partner', string="Participante", domain="[('es_participante', '=', True)]")
    
    name = fields.Char(string="Nombre del Documento", required=True)
    document_file = fields.Binary(string="Archivo PDF", required=True)
    document_type_id = fields.Many2one('infocap.tipo.documento', string="Tipo de Documento", required=True)
    tipo_accionformativa_id = fields.Many2one('infocap.tipo.accionformativa', string="TIPO ACCIÓN FORMATIVA")
    acciones_formativas_ids = fields.One2many('infocap.acciones.formativas', 'tipo_accionformativa_id', string='ACCIONES FORMATIVAS')
    talleres_ids = fields.One2many('infocap.talleres', 'tipo_taller', string='TALLERES')
    talleres_id = fields.Many2one('infocap.talleres', string="Taller", required=True, ondelete='cascade')
    tipo_taller_id = fields.Many2one('infocap.tipo.taller', string="TIPO TALLER")
    
   
    solicitudes_id = fields.Many2one('crm.lead', string="Solicitudes asociadas")

    horas_dia = fields.Float('HORAS') # Horas del taller del dia
    fecha = fields.Date('Fecha valor', required=True) # Dia del rango del taller
    
    

    

    