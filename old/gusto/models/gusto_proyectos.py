
from odoo import models, fields, api


class GustoProyectos(models.Model):
    _name = 'gusto.proyectos'
    _description = 'Registro de proyectos'


    name = fields.Char('Proyecto')
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincia_ids = fields.Many2many('res.country.state', string="Provincias", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='EMPRESAS',required=False,)#default=lambda self: self.env.company)
    #denominacion = fields.Char('Proyecto')
    situacion = fields.Selection([('abierto','ABIERTO'), ('cerrado','CERRADO'),], string="Estado")
    observaciones = fields.Char('Observaciones')
    
    
    programas_ids = fields.One2many('gusto.programas', 'proyecto_id', string='Programas')
    
    




    