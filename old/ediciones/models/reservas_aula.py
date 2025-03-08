# -*- coding: utf-8 -*-
from odoo import models, fields, api

# models/aula.py
class reservas.Aula(models.Model):
    _name = 'reservas.aula'
    _description = 'Gestión de Aulas'
    
    name = fields.Char(string='Nombre del Aula', required=True)
    ubicacion_id = fields.Many2one('stock.location', string='Ubicación')
    capacidad = fields.Integer(string='Capacidad')
    reservas_ids = fields.One2many('aula.reserva', 'aula_id', string='Reservas')
    ocupacion = fields.Float(string='Grado de Ocupación (%)', compute='_compute_ocupacion')

    @api.depends('reservas_ids')
    def _compute_ocupacion(self):
        for aula in self:
            total_horas = sum(aula.reservas_ids.mapped('horas_reserva'))
            aula.ocupacion = (total_horas / (8 * len(aula.reservas_ids))) * 100 if aula.reservas_ids else 0

