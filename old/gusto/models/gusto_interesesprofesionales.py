
from odoo import models, fields, api


class GustoInteresesprofesionales(models.Model):
    _name = 'gusto.interesesprofesionales'
    _description = 'Tabla auxiliar Intereses Profesionales'



    name = fields.Char('INTERESES PROFESIONALES')
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company)
    




    