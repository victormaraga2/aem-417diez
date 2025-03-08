# -*- coding: utf-8 -*-

from odoo import models, fields, api, _



class CaptacionTipoTag(models.Model):
    _name = 'captacion.tipo.tag'
    _description = 'Tipo Tag'

    name = fields.Char(string='Name', required=True)
    categoria_id = fields.Many2one('captacion.categoria.tag', string='Categoria', required=True)

    nivel_sino = fields.Boolean(related='categoria_id.nivel_sino', store=True)
    experiencia = fields.Boolean(related='categoria_id.experiencia' , store=True)
