# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date, timedelta


class InfocapParticipantes(models.Model):

    # _name = 'infocap_participantes'
    #_inherit = 'mail.thread'
    _inherit = 'res.partner'
    _description = 'Registro de Participantes'

    # Para participantes
    #
    es_participante = fields.Boolean(string="Es Participante", default=True)
    estado_participante = fields.Selection(string="Estado", default="participando",
                             selection=[('participando', 'Participando'),
                                        ('solicitando', 'Solicitando')])

    
    country_id = fields.Many2one('res.country', string='PAÍS', default=lambda self: self.env.ref('base.es'))
    state_id = fields.Many2one('res.country.state', string='Provincia', domain="[('country_id', '=', country_id)]")                                    

    # programa_id = fields.Many2one('infocap.programas', string='Programa')
    # proyecto_id = fields.Many2one('infocap.proyectos', string='Proyecto', domain="[('programas_id', '=', programas_id)]")
 
    # convocatoria_id = fields.Many2one('infocap.convocatoria', string='Convocatoria', domain="[('proyectos_id', '=', proyectos_id)]")
    solicitudes_ids = fields.One2many('crm.lead', 'partner_id', string='Solicitudes')
    productos_ids = fields.Many2many('product.product', string='Solicitud')

   
    #producto_id = fields.Many2one(
    #'product.product',
    #string='Solicita participar',
    #domain="[('convocatoria_ids', 'in', convocatoria_id)]")
    
    alta_sto=fields.Date('F. ALTA STO')                                 #   STO -> FECHA INICIO
    baja_sto=fields.Date('F. BAJA STO')                                 #   STO -> FECHA FIN
    colectivo=fields.Many2one('infocap.colectivo', index=True)          #   STO -> COLECTIVO
    inicio_atencion=fields.Date('INICIO ATENCIÓN')                      #   STO -> FECHA INICIO ATENCION
    fin_atencion=fields.Date('FIN ATENCIÓN')                            #   STO -> FECHA FIN ATENCION
    recibi=fields.Date('INCENTIVO')                                     #   STO -> FECHA RECIBI
    inicio_inserccion=fields.Date('INICIO INSERCCIÓN')                  #   STO -> FECHA INICIO INSERCCION
    fin_inserccion=fields.Date('FIN INSERCCIÓN')                        #   STO -> FECHA FIN INSERCCION
    


    ####  RELACIONES  ##########
    #     MODELOS / ENTIDADES 
    ############################

    
    documentos_ids = fields.One2many('infocap.documentos', 'participante_id', string='DOCUMENTOS')
    
    
    ####  RELACIONES  ##########
    #     PARAMETRICAS 
    ############################
    sector_ocupacion=fields.One2many('infocap.sectores.participantes','participante_id',string='SECTOR OCUPACIÓN')
    perfil_ocupacion_ids=fields.One2many('infocap.perfiles.participantes','participante_id',string='PERFIL OCUPACIÓN')

    
    
    # VALORES AUXILIARES NUMERICOS PARA CALCULOS Y KPI


    vcv = fields.Binary() # !!!!!    OJO    !!!!! ESTAN CAMBIADOS
    vlab = fields.Binary() # !!!!!    OJO    !!!!! ESTAN CAMBIADOS
  
    formador_previsto = fields.Char()
    integrador_previsto = fields.Char()
    formador_real = fields.Char()
    integrador_real = fields.Char()


    ####  CAMPOS % AVANCE ARRASTRADOS DE :
    ####  - ORIENTACION INICIAL         10H
    ####  - LAS ACCIONES FORMATIVAS     50H
    ####  - TALLERES                    
    ####  - ANEXAS
    ####  - ORIENTACION A LA INSERCCION 40H


    
    finaliza_accion = fields.Boolean(string='FINALIZA', default='True')
    fecha_valor=fields.Date('FECHA ACTUALIZACION STO') 
    fecha_objetivo = fields.Date('FECHA OBJETIVO') #, compute='_compute_fecha_objetivo', store=True) 
    fecha_real = fields.Date('FECHA REAL')
    prosp_integra_prev_id = fields.Many2one('infocap.prospectores', string='INTEGRADO POR')

    def prueba(self):
        print('prueba')
        return True

    def unlink(self):
        leads = self.env['crm.lead'].search([('partner_id', 'in', self.ids)])
        self.es_participante = False
        for record in self:
            record.es_participante = False  # Poner es_participante en False antes de borrar
            

            
        result = super(InfocapParticipantes, self).unlink()  # Borrar el contacto

        # Actualizar los leads relacionados para reflejar que el contacto ya no existe
        for lead in leads:
            lead.is_contact_created = False  # Indicar que el contacto ya no existe
            lead.stage_id = 3  # Volver a poner el lead en "Nuevo"
        
        return result

    