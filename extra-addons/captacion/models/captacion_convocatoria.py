
from odoo import models, fields, api


class CaptacionConvocatoria(models.Model):
    _name = 'captacion.convocatoria'
    _description = 'Registro de comvocatoria'


    name = fields.Char('DENOMINACION')
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincias_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='EMPRESAS',required=False,)#default=lambda self: self.env.company)
    denominacion = fields.Char('DENOMINACION')
    situacion = fields.Selection([('abierto','ABIERTO'), ('cerrado','CERRADO'),], string="ESTADO")
    observaciones = fields.Char('Observaciones')
    
    fecha_inicio = fields.Date('FECHA INICIO')
    fecha_fin = fields.Date('FECHA FIN')
   
    programa_id = fields.Many2one('captacion.programas', string='PROGRAMA')
    #participantes_ids = fields.One2many('captacion.participantes','convocatoria_par_id',string='PARTICIPANTES')
    #solicitudes_ids = fields.One2many('captacion.solicitudes','convocatoria_sol_id',string='SOLICITUDES')
    
    




    