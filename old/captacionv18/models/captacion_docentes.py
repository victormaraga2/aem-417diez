
from odoo import models, fields, api


class CaptacionDocentes(models.Model):
    _name = 'captacion.docentes'
    _description = 'Registro de docentes'


    name=fields.Char('docentes')
