from odoo import models, fields, api, _
import re
from datetime import timedelta
from odoo.exceptions import ValidationError


class infocapTalleres(models.Model):
    _name = 'infocap.talleres'
    _description = 'Registro de talleres'

    talleres_id = fields.Integer(string='ID')

    
    #####################################################

    tipo_taller = fields.Many2one('infocap.tipo.taller','TIPO TALLER')
    name = fields.Char('DENOMINACION')    
    id_sto = fields.Integer('ID_STO')
    country_id = fields.Many2one('res.country', string='País', default=lambda self: self.env.ref('base.es'))
    provincia_id = fields.Many2one('res.country.state',  
                                   domain="[('country_id', '=', country_id), ('name', 'in', ['Cádiz', 'Córdoba', 'Granada', 'Huelva', 'Jaén', 'Málaga', 'Sevilla', 'Almería'])]",
                                   string='PROVINCIA')
    
    user_id = fields.Many2one('res.users', string='Usuario', default=lambda self: self.env.user)
    
    
    provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
        
    fec_inicio = fields.Date('F. INICIO')
    fec_fin = fields.Date('F. FIN')
    horas = fields.Float('HORAS') # Horas totales del taller 
    turno = fields.Char('TURNO MÑN-TARDE')
    aula = fields.Char('AULA') ## Aula del taller
    observaciones = fields.Char('Observaciones')
    modalidad = fields.Selection([('individual', 'Individual'), ('grupal', 'Grupal')], default='grupal', required=True, string='MODALIDAD')
    finaliza = fields.Boolean(string="Finaliza Taller", default=True)

    
    participantes_talleres_ids = fields.Many2many('res.partner', relation='participante_talleres3_rel', string='PARTICIPANTES')
    participante_id = fields.Many2one('res.partner', string='PARTICIPANTE')
    # participantes_talleres_finaliza = fields.One2many('infocap.participantes.talleres.finaliza', 'taller_id', string="Participante Finaliza Taller")
    

    documentos_ids = fields.One2many('infocap.documentos', 'participante_id', string='DOCUMENTOS')

    
    def prueba2(self):
        print('prueba')
        return True

    
    
    