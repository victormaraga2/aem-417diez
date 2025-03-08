
from odoo import models, fields, api


class CaptacionOportunidad(models.Model):
    #_name = 'crm_captacion.participantes'
    _description = 'Registro de participantes'
    _inherit = 'crm.lead'



    proyecto_id = fields.Many2one('captacion.proyectos', string='Proyecto')
    #proyecto = fields.Selection(selection=[], compute="_compute_proyecto", string="Proyecto", store=True)
    programa_id = fields.Many2one('captacion.programas', string='Programa', domain="[('proyecto_id', '=', proyecto_id)]" )
    #programa = fields.Selection(selection=[], compute="_compute_programa", string="Programa", store=True)
    convocatoria_id = fields.Many2one('captacion.convocatoria', string='Convocatoria', domain="[('programa_id', '=', programa_id)]")

    # producto_id = fields.Many2one('product.product', string= 'Solicita participar', domain="[('convocatia_id', '=', convocatoria_id)]")
    producto_id = fields.Many2one(
    'product.product',
    string='Solicita participar',
    domain="[('convocatoria_ids', 'in', convocatoria_id)]"
)
    #producto_id_name = fields.Char( related = 'producto_id.name', string= 'Producto')
    name = fields.Char(compute='_compute_asunto')




    @api.onchange('producto_id') 
    def _compute_asunto(self):
        for rec in self:
            rec.name = rec.producto_id.name
    #        a = 0
 

    #@api.depends('proyecto_id')
    #def _compute_proyecto(self):
    #    for record in self:
    #        if record.proyecto_id:
    #            record.proyecto = record.proyecto_id.name
    #        else:
    #            record.tipo_proyecto = False
    
    #@api.depends('programa_id')
    #def _compute_programa(self):
    #    for record in self:
    #        if record.programa_id:
    #            if record.programa_id.proyecto_id == record.proyecto_id.id:
    #                record.programa = record.programa_id.name
    #        else:
    #            record.programa = False




    