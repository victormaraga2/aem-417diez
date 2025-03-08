
from odoo import models, fields, api


class InfocapTipoDocumento(models.Model):
    _name = 'infocap.tipo.documento'
    _description = 'Registro de tipo documento'


    name = fields.Char(string="Tipo de Documento", required=True)


    