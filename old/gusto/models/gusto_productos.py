
from odoo import models, fields, api


class GustoProductos(models.Model):
    _description = 'Registro de productos'
    _inherit = 'product.product'



    proyecto_id = fields.Many2many('gusto.proyectos', string='Proyecto')

    programa_id = fields.Many2one('gusto.programas', string='Programa')

    #3 convocatoria_ids = fields.One2many('gusto.convocatoria', 'producto_id',  string='Convocatoria', )

    convocatoria_ids = fields.Many2many('gusto.convocatoria', string='Convocatorias')

    
