from odoo import models, fields, api, _
from datetime import datetime, date, timedelta


class InfocapProductosConvocatorias(models.Model):
    _name = 'infocap.productos_convocatorias'
    _description = 'Productos de Convocatorias'

    producto_id = fields.Many2one('product.product', string='Curso', required=True)
    provincia_id = fields.Many2one('infocap.provincias', string='Provincia')
    nparticipantes = fields.Integer(string='Número de Participantes', required=True)    
    convocatoria_id = fields.Many2one('infocap.convocatoria', string='Convocatoria', required=True, ondelete='cascade')
    # Se incluye el campo fecha para preever ampliaciones de la convocatoria 
    observaciones = fields.Char('Observaciones')
    fecha = fields.Date('Fecha')
