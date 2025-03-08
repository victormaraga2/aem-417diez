
from odoo import models, fields, api


class CaptacionProgramas(models.Model):
    _name = 'captacion.programas'
    _description = 'Registro de programas'


    name = fields.Char('DENOMINACION')
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company)
    denominacion = fields.Char('DENOMINACION')
    situacion = fields.Selection([('abierto','ABIERTO'), ('cerrado','CERRADO'),], string="ESTADO")
    observaciones = fields.Char('Observaciones')
    
    
    proyecto_id = fields.Many2one('captacion.proyectos', string='PROYECTOS')
    
    convocatorias_ids = fields.One2many('captacion.convocatoria','programa_id', string='CONVOCATORIA')
    
    
    




    