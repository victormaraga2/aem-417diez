
from odoo import models, fields, api


class InfocapProductos(models.Model):
    _description = 'Registro de productos'
    _inherit = 'product.product'



    proyecto_id = fields.Many2many('infocap.proyectos', string='Proyecto')
    programa_id = fields.Many2one('infocap.programas', string='Programa')
    convocatoria_ids = fields.Many2many('infocap.convocatoria', string='Convocatorias')
    convocatoria_id = fields.Many2one('infocap.convocatoria', string="Convocatoria")

    
