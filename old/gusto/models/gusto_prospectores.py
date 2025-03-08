
from odoo import models, fields, api


class GustoProspectores(models.Model):
    _name = 'gusto.prospectores'
    #_inherit = 'mail.thread'
    _description = 'Registro de prospectores'


    name=fields.Char('PARTNER')
    telefono=fields.Char('TELEFONO')
    correo=fields.Char('CORREO')
    es_externo = fields.Boolean('EXTERNO', default=True)

    ### Campos añadidos por Victor ### 14/01/2025
    ####################################################
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company)
    ####################################################
   
    #### RELACIONES
    #document_ids = fields.One2many('gusto.documentos', 'prospector_id', string="Documentos PDF")
    docaem_ids = fields.One2many('gusto.docaem', 'gusto_id', string='Documentos')
    acciones_formativas_ids = fields.One2many('gusto.acciones.formativas', 'prospector_id', string="Acciones Formativas")
    # contratos_ids = fields.One2many('gusto.contratos', 'prospector_id', string='Contratos')
   
    contratos_ids = fields.One2many('gusto.contratos','partner_integrador', string='Contratos', order='participante_id desc' ) #'prospector_id', string='Contratos')
    total_contratos = fields.Integer(compute='_compute_totales', string="TOTAL CONTRATOS")
    total_participantes = fields.Integer(compute='_compute_totales', string="TOTAL PPARTICIPANTES")
    total_modalidades = fields.Integer(compute='_compute_totales', string="MODALIDADES")


    @api.depends('contratos_ids')
    def _compute_totales(self):
        for rec in self:
            # Contar el total de contratos
            rec.total_contratos = len(rec.contratos_ids)
            
            # Obtener los valores únicos de id_participante
            participantes_unicos = rec.contratos_ids.mapped('participante_gusto')
            rec.total_participantes = len(set(participantes_unicos))
            
            # Obtener los valores únicos de modalidad
            modalidades_unicas = rec.contratos_ids.mapped('modalidad')
            rec.total_modalidades = len(set(modalidades_unicas))
