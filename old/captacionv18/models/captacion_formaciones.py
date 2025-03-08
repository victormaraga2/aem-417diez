from odoo import models, fields

class CaptacionFormaciones(models.Model):
    _name = 'captacion.formaciones'
    _description = 'Tipo Formaciones'

    
    captacion_id = fields.Many2one('res.partner', string="Participante")
    tipo_formacion = fields.Many2one('captacion.tipo.formacion', string="Tipo")
    accion_id = fields.Many2one('captacion.acciones.formativas', string="Accion Formativa")
    taller_id = fields.Many2one('captacion.talleres', string="Taller")
    fecha_inicio = fields.Date('Inicio')
    fecha_fin = fields.Date("Fin")
    horas = fields.Float('Horas')
    #docaem_ids = fields.Many2many('captacion.docaem')
    
    