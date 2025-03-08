
from odoo import models, fields, api


class CaptacionProductos(models.Model):
    _description = 'Registro de productos'
    _inherit = 'product.product'



    proyecto_id = fields.Many2many('captacion.proyectos', string='Proyecto')

    programa_id = fields.Many2one('captacion.programas', string='Programa')

    #3 convocatoria_ids = fields.One2many('captacion.convocatoria', 'producto_id',  string='Convocatoria', )

    convocatoria_ids = fields.Many2many('captacion.convocatoria', string='Convocatorias')

    
