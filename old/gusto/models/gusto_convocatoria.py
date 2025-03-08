
from odoo import models, fields, api


class GustoConvocatoria(models.Model):
    _name = 'gusto.convocatoria'
    _description = 'Registro de comvocatoria'


    name = fields.Char('Convocatoria')
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincias_ids = fields.Many2many('res.country.state', string="Provincias", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='EMPRESAS',required=False,)#default=lambda self: self.env.company)
    #denominacion = fields.Char('Convocatoria')
    situacion = fields.Selection([('abierto','ABIERTO'), ('cerrado','CERRADO'),], string="Estado")
    observaciones = fields.Char('Observaciones')
    
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
   
    proyecto_id = fields.Many2one('gusto.proyectos', string='Proyecto')
    programa_id = fields.Many2one('gusto.programas', string='Programa')

    productos_ids = fields.Many2many('product.product', string='Solicitud')

    producto_id = fields.Many2one(
        'product.product', 
        string='Producto'
    )

    #participantes_ids = fields.One2many('gusto.participantes','convocatoria_par_id',string='PARTICIPANTES')
    
    #solicitudes_ids = fields.One2many('gusto.solicitudes','convocatoria_sol_id',string='SOLICITUDES')
    
    




    