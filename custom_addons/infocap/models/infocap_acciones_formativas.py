
from odoo import models, fields, api, exceptions, _
import re
from datetime import timedelta


class infocapAccionesFormativas(models.Model):
    _name = 'infocap.acciones.formativas'
    #_inherit = 'mail.thread'
    _description = 'Registro de acciones formativas sto'



    id_sto = fields.Integer('ID STO')
    name = fields.Char('Nº AF')
    nexp = fields.Char('Nº EXP Vº Bº')
    country_id = fields.Many2one('res.country', string='PAÍS', default=lambda self: self.env.ref('base.es'))
    provincia_ids = fields.Many2many('res.country.state', string='Provincia', domain="[('country_id', '=', country_id)]")

    #provincia_ids = fields.Many2many(
    #    'res.country.state', 
    #    string='PROVINCIA',
    #    domain="[('country_id', '=', country_id), ('name', 'in', ['Cádiz', 'Córdoba', 'Granada', 'Huelva', 'Jaén', 'Málaga', 'Sevilla', 'Almería'])]")
    
    user_id = fields.Many2one('res.users', string='Tecnico', default=lambda self: self.env.user)

    company_id = fields.Many2one(
        'res.company', string="Empresa", default=lambda self: self.env.company, required=True
    )

    
    #####################################################
    
    
    fec_inicio = fields.Date(string='INICIO AF')               
    fec_fin = fields.Date(string='FIN AF')                     
    tipo_accionformativa_id = fields.Many2one('infocap.tipo_accionformativa', string='TIPO ACCION')
  
    nombreaccion = fields.Char('NOMBRE DE LA ACCION')
    modalidad = fields.Selection([('online', 'On line'), ('presencial', 'Presencial')], string='MODALIDAD')
    
    dinamizador_id = fields.Many2one('res.partner', string='DINAMIZADOR', domain="[('es_dinamizador_colaborador', '=', True)]")
    formador_id = fields.Many2one('res.partner', string='EMPRESA FORMADORA', domain="[('es_empresa_formadora', '=', True)]")
    docente_ids = fields.Many2many('res.partner', relation='infocap_docentes_rel', string='DOCENTE', domain="[('es_docente', '=', True)]")

    recurso = fields.Selection(string='RECURSO', selection=[('interno','INTERNO'),('externo','EXTERNO')])
    horas = fields.Float('HORAS ACCION')
    participantes_accionformativa_ids = fields.Many2many('res.partner', relation='infocap_participantes_rel', string='PARTICIPANTES', domain="[('es_participante', '=', True)]")
    estado = fields.Selection(string='ESTADO', selection=[('planificado','PLANIFICADO'),('activo','ACTIVO'),('cancelado','CANCELADO')])

    contrata_prev = fields.Integer(string='CONTRATACIONES PREV')
    contrata_real = fields.Integer(string='CONTRATACIONES REAL')
    
    n_part_prev = fields.Integer('Nº PART. PREV.')
    n_part_real = fields.Integer('Nº PART. REAL')
    
    presupuesto_solicitado = fields.Float('PRESUPUESTO SOLICITADO')
    coste = fields.Float('COSTE')
    pendiente_justificar = fields.Float('PENDIENTE JUSTIFICAR')
    
    validacion = fields.Boolean('VALIDACIÓN')
    observaciones = fields.Char('OBSERVACIONES')

    documentos_ids = fields.One2many('infocap.documentos', 'participante_id', string='DOCUMENTOS')

    
    
    

    