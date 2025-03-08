
from odoo import models, fields, api


class CaptacionTipoDocumento(models.Model):
    _name = 'captacion.tipo.documento'
    _description = 'Registro de tipo documento'


    name = fields.Char(string="Tipo de Documento", required=True)


    