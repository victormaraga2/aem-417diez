# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ReservasAulaReserva(models.Model):
    _name = 'reservas.aula.reserva'
    _description = 'Reservas de Aulas'

    aula_id = fields.Many2one('reservas.aula', string='Aula', required=True)
    fecha_inicio = fields.Datetime(string='Fecha y Hora de Inicio', required=True)
    fecha_fin = fields.Datetime(string='Fecha y Hora de Fin', required=True)
    tipo_reserva = fields.Selection([
        ('mañana', 'Solo Mañana'),
        ('tarde', 'Solo Tarde'),
        ('dia_completo', 'Día Completo')
    ], string='Tipo de Reserva', required=True)
    usuario_id = fields.Many2one('res.users', string='Reservado por', required=True)
    proyecto_id = fields.Many2one('project.project', string='Proyecto')
    horas_reserva = fields.Float(string='Horas Reservadas', compute='_compute_horas_reserva')

    @api.depends('fecha_inicio', 'fecha_fin')
    def _compute_horas_reserva(self):
        for reserva in self:
            if reserva.fecha_inicio and reserva.fecha_fin:
                delta = reserva.fecha_fin - reserva.fecha_inicio
                reserva.horas_reserva = delta.total_seconds() / 3600
