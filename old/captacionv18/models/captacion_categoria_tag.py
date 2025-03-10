# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CaptacionCategoriaTag(models.Model):
    _name = 'captacion.categoria.tag'
    _description = 'Categoria Tag'

    name = fields.Char(string='Name', required=True)
    nivel_sino = fields.Boolean(string='Nivel', default=False)
    experiencia = fields.Boolean(string='Experiencia', default=False)
