
from odoo import models, fields, api


class GustoProcedenciaentrada(models.Model):
    _name = 'gusto.procedenciaentrada'
    _description = 'Tabla auxiliar Procedencia Entrada '



    name = fields.Char('PROCEDENCIA ENTRADA')
    #company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    




    