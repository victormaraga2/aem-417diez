
from odoo import models, fields, api


class CaptacionDocumentos(models.Model):
    _name = 'captacion.documentos'
    _description = 'Registro de documentos'


    name = fields.Char(string="Nombre del Documento", required=True)
    document_file = fields.Binary(string="Archivo PDF", attachment=True, required=True)
    document_type_id = fields.Many2one('captacion.tipo.documento', string="Tipo de Documento", required=True)
    fecha = fields.Date('Fecha valor', required=True)
    captacion_id = fields.Many2one('res.partner', string="Participante", ondelete='cascade')

    prospector_id = fields.Many2one('captacion.prospectores', string="Prospector", ondelete='cascade')


    

    