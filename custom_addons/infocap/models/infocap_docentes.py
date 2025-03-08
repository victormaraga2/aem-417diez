# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date, timedelta


class InfocapDocentes(models.Model):

    #_inherit = 'mail.thread'
    _inherit = 'res.partner'
    _description = 'Registro de Docentes'

    # Para partner
    es_docente = fields.Boolean(string="Es Docente", default=True)
    estado_docente = fields.Selection(string="Estado", default="libre",
                             selection=[('libre', 'Libre'),
                                        ('ocupado', 'Ocupado'),
                                        ('otro', 'Otro')])
    proyecto_id = fields.Many2one('infocap.proyectos', string='Proyecto')
    programa_id = fields.Many2one('infocap.programas', string='Programa', domain="[('proyecto_id', '=', proyecto_id)]" )
    convocatoria_id = fields.Many2one('infocap.convocatoria', string='Convocatoria', domain="[('programa_id', '=', programa_id)]")

   
    producto_id = fields.Many2one(
    'product.product',
    string='Docente de',
    domain="[('convocatoria_ids', 'in', convocatoria_id)]")
    


    ####  RELACIONES  ##########
    #     MODELOS / ENTIDADES 
    ############################

    # contratos_ids = fields.One2many('infocap.contratos','participante_id', string='DNI')
    # acciones_formativas_id = fields.Many2one('infocap.acciones.formativas', string="Nº AF")
    documentos_ids = fields.One2many('infocap.documentos', 'participante_id', string='DOCUMENTOS')
    # talleres_dinamizador_ids = fields.Many2many('infocap.talleres', relation='infocap_talleres1_rel', string='TALLERES_GRUP') 
    #talleres_dinamizador2_ids = fields.One2many('infocap.talleres', 'participante_id',string='TALLERES_IND')

    # talleres_id = fields.Many2one('infocap.talleres', string='PARTICIPANTES')

       
    ## Onetomany a participantes
    # prosp_integra_prev_id = fields.Many2one('infocap.prospectores', string='INTEGRADO POR')


    
    
    