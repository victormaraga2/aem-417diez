from odoo import models, fields

class CaptacionTipoFormacion(models.Model):
    _name = 'captacion.tipo.formacion'
    _description = 'Tipo Formacion'

    name = fields.Char(string='Tipo Formacion', required=True)