# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
import logging
_logger = logging.getLogger(__name__)

class GustoGusto(models.Model):
    #_name = 'gusto.gusto'
    #_inherit = 'mail.thread'
    _inherit = 'res.partner'
    _description = 'Regis#ro de gusto sto'

    
    name=fields.Char('DNI/NIE', index=True)                            #   STO -> NIF/NIE
    provincia=fields.Char(string='PROVINCIA', index=True)                     #   STO -> PROVINCIA
    participante=fields.Char('PARTICIPANTE', index=True)               #   STO -> PARTICIPANTE
    pt_nombre=fields.Char('PT. NOMBRE')                    #   STO -> PT. NOMBRE
    pt_apellido1=fields.Char('PT. APELLIDO1')              #   STO -> PT. APELLIDO1
    pt_apellido2=fields.Char('PT. APELLIDO2')              #   STO -> PT. APELLIDO1
    unidad=fields.Char('UNIDAD')                           #   STO -> UNIDAD
    alta_sto=fields.Date('F. ALTA STO')                    #   STO -> FECHA INICIO
    baja_sto=fields.Date('F. BAJA STO')                    #   STO -> FECHA FIN
    colectivo=fields.Many2one('gusto.colectivo', index=True)           #   STO -> COLECTIVO
    inicio_atencion=fields.Date('INICIO ATENCIÓN')         #   STO -> FECHA INICIO ATENCION
    fin_atencion=fields.Date('FIN ATENCIÓN')               #   STO -> FECHA FIN ATENCION
    h_orienta=fields.Char('H. ORIENTACIÓN')                #   STO -> H. HORIENTA
    h_forma=fields.Char('H. FORMACIÓN')                    #   STO -> H. FORMACION
    recibi=fields.Date('INCENTIVO')                        #   STO -> FECHA RECIBI
    inicio_inserccion=fields.Date('INICIO INSERCCIÓN')     #   STO -> FECHA INICIO INSERCCION
    fin_inserccion=fields.Date('FIN INSERCCIÓN')           #   STO -> FECHA FIN INSERCCION
    h_fase_inserccion=fields.Char('H. FASE INSERCCIÓN')    #   STO -> H. FASE INSERCCION -> ACTUAL OI4OH
    d_fase_inserccion=fields.Char('D. FASE INSERCCIÓN')    #   STO -> D. FASE INSERCCION -> NUEVO
    id_participante_sto = fields.Integer('ID_STO', index=True)         #   PREVISTO STO
    dias_fase_insercion = fields.Integer('DIAS F. INSERCION')  #   STO -> DIAS FASE INSERCCION
    

    ### Campos añadidos por Victor ### 14/01/2025
    #######################################################
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company
    #######################################################


    ######################################################################################################
    #
    # CAMPOS AUXILIARES
    #
    ######################################################################################################
    # PENDIENTE -> CONECTAR CON PROYECTO 
    # PENDIENTE -> INCLUIR ID PROYECTO
    # PENDIENTE -> PREVEER CONECION CON UNIDAD -> ute
    # PENDIENTE -> INCLUIR ID UTE
    # 

    municipio=fields.Char('MUNICIPIO')                     ##########       GUSTO
    foto_participante=fields.Binary("FOTO")                ##########       GUSTO
    telefono=fields.Char("TELÉFONO")                       ##########       GUSTO
    correo=fields.Char("CORREO")                           ##########       GUSTO
    anos_exp=fields.Char('AÑOS EXP')                       ##########       GUSTO
    observacion = fields.Char("OBSERVACIÓN")               ##########       GUSTO
    #larma = fields.Boolean(string="AV.", default=False)   ##########       GUSTO
    
            
    ###### ESTADOS Y CAMPOS CALCULADOS  ####
    #
    #   FASE 1 = ATENDIDA
    #   ALTA STO + H.HORIENTACION >= 10H + H. FORMACION >= 50H (SE OBTIENEN DE ACCIONES FORMATIVAS)
    #
    #   ALARMA RECIBI = FECHA FIN ATENCION + 90 DÍAS (SE APLICA A 75 DIAS PARA TENER MARGEN Parametrizable) RECOPILAR DOCUMENTACION
    #
    #   FASE 2 = INSERCCION
    #
    #   FECHA INICIO INSERCCION = FECHA FIN ATENCION + 1 DIA
    #   OI40H > 40H (SE OBTIENEN DE TALLERES) + RECIBI (RECOPILAR DOCUMENTADO) + 120 DIAS COMPUTABLES -> SE OBTIENEN DE CONTRATOS
    #   RECIBI CON FECHA 8DEBE ESTAR EN TIEMPO)
    # 
    #   RESULTADO
    #   INSERTADO =  FASE 1 ATENDIDA + FASE 2 INSERCCION
    #   NO INSERTADO = FASE 1 ó FASE 2 NO COMPLETAS
    #

    q_participante = fields.Integer(string='PARTICIPANTES STO', compute="_compute_estadisticas", store=True)
    q_baja = fields.Integer(string='BAJA STO', compute="_compute_estadisticas", store=True)
    q_orientacion = fields.Integer(string='ORIENTACION', compute="_compute_estadisticas", store=True)
    q_persona_atendida = fields.Integer(string='PERSONA ATENDIDA', compute="_compute_estadisticas", store=True)
    q_incentivo = fields.Integer(string='INCENT.PAGADO', compute="_compute_estadisticas", store=True)
    q_oi40h = fields.Integer(string='OI 40H', compute="_compute_estadisticas", store=True)
    q_insertados = fields.Integer(string='INSERTADOS', compute="_compute_estadisticas", store=True)
    q_prioritarios = fields.Integer(string='PRIORITARIOS', compute="_compute_estadisticas", store=True)
    qt_insertados = fields.Boolean(string='INSERTADOS', compute="_compute_estadisticas", store=True)
    qt_prioritarios = fields.Boolean(string='PRIORITARIOS', compute="_compute_estadisticas", store=True)
    q_isosinoi = fields.Integer(string='ISO SIN OI', compute="_compute_estadisticas", store=True)
    q_isoconoi = fields.Integer(string='ISO CON OI', compute="_compute_estadisticas", store=True)
    q_participanter = fields.Integer(string='PSTO', compute="_compute_estadisticas", store=True)
    q_participantef = fields.Integer(string='FSTO', compute="_compute_estadisticas", store=True)


    fase_orienta=fields.Char('FASE OORIENTACIÓN')          ############     CALCULADO STO
    est_orientacion = fields.Selection(string='ORIENTACIÓN I.', selection=[('noinciada','NO INICIADA'),('encurso','EN CURSO'),('finalizada', 'FINALIZADA')], compute='_compute_estados', store=True)
    est_formacion = fields.Selection(string='FORMACIÓN', selection=[('noinciada','NO INICIADA'),('encurso','EN CURSO'),('finalizada', 'FINALIZADA')], compute='_compute_estados', store=True)
    est_inserccion = fields.Selection(string='INSERCCIÓN', selection=[('noinciada','NO INICIADA'),('encurso','EN CURSO'),('finalizada', 'FINALIZADA')], compute='_compute_estados', store=True)
    est_incentivo = fields.Selection(string='INCENTIVO', selection=[('si','SÍ'),('no','NO')], compute="_compute_estados", store=True)
    est_orientacion40 = fields.Selection(string='ORIENTACION 40h', selection=[('noinciada','NO INICIADA'),('encurso','EN CURSO'),('finalizada', 'FINALIZADA')], compute="_compute_estados", store=True)
    diastrabajado = fields.Integer('DIAS TRABAJADOS', compute="_compute_sum_dias", store=True) #compute="_compute_sum_dias_trabajado", store=True)       ####   ARRASTRAR DE CONTRATOS
    diascomputable = fields.Integer('DIAS COMPUTABLES', compute="_compute_sum_dias", store=True) # compute="_compute_sum_dias_computado", store=True)       #   ARRASTRAR DE CONTRATOS
    peonadasc = fields.Integer('PEONADAS COMP.',compute="_compute_sum_dias", store=True)  #compute="_compute_sum_dias_computado", store=True) 

    h_orienta_gus = fields.Float('H.ORIENTACION' , compute='_compute_horas_gusto', store=False)
    h_ori_ins_gus = fields.Float('H.O.INSERCION', compute='_compute_horas_gusto', store=False)
    h_anexo_gus = fields.Float('H. T. ANEXO', compute='_compute_horas_gusto', store=False)
    h_anexo3_gus = fields.Float()
    es_agrario = fields.Boolean('1.-TIENE CONTRATO AGRARIO',compute='_compute_sum_dias', store=True)
    es_parcial = fields.Boolean('2.-SIN CONTRATO PARCIAL',compute='_compute_sum_dias', store=True)



    
   

    ####  RELACIONES  ##########
    #     MODELOS / ENTIDADES 
    ############################

    contratos_ids = fields.One2many('gusto.contratos','participante_id', string='DNI')
    acciones_formativas_id = fields.Many2one('gusto.acciones.formativas', string="Nº AF")
    docaem_ids = fields.One2many('gusto.docaem', 'gusto_id', string='DOCUMENTOS')
    talleres_gusto_ids = fields.Many2many('gusto.talleres', relation='gusto_talleres1_rel', string='TALLERES_GRUP') 
    talleres_gusto2_ids = fields.One2many('gusto.talleres', 'gusto_id',string='TALLERES_IND')

    talleres_id = fields.Many2one('gusto.talleres', string='PARTICIPANTES')

    ####  RELACIONES  ##########
    #     PARAMETRICAS 
    ############################
    sector_ocupacion=fields.One2many('gusto.sectores.participantes','participante_id',string='SECTOR OCUPACIÓN')
    perfil_ocupacion_ids=fields.One2many('gusto.perfiles.participantes','participante_id',string='PERFIL OCUPACIÓN')
    tag_ids = fields.One2many('gusto.tag', 'gusto_id', string='TAGS')
    acciones_idsto =fields.Integer( related='acciones_formativas_id.id_sto')
    acciones_accion =fields.Char( related='acciones_formativas_id.nombreaccion')
    acciones_horas =fields.Float( related='acciones_formativas_id.horas')
    acciones_fecini =fields.Date( related='acciones_formativas_id.inicio')
    acciones_fecfin =fields.Date( related='acciones_formativas_id.fin')
    
    # VALORES AUXILIARES NUMERICOS PARA CALCULOS Y KPI

    espacio=fields.Char()
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
    prosp_integra_prev_id = fields.Many2one('gusto.prospectores', string='INTEGRADO POR')


    pasap = fields.Integer(string="Valor Devuelto del Taller")
    
    # trigger_on_form_load = fields.Boolean(string="Trigger", default=True)

    """
    ############# Añadido por Víctor 15/01/2025 ###################
    ###############################################################
    @api.model
    def create(self, vals):
        # Crea el registro
        record = super(GustoGusto, self).create(vals)

        # Transfiere los datos del campo Many2many al campo One2many
        record._transferir_talleres_automatica()

        return record

    def write(self, vals):
        # Actualiza el registro
        result = super(GustoGusto, self).write(vals)

        # Transfiere los datos del campo Many2many al campo One2many
        self._transferir_talleres_automatica()

        return result
    """
 #   def _transferir_talleres_automatica(self):
 #       for record in self:
 #           # Paso 1: Limpiar el campo One2many antes de cargar nuevos datos
 #           record.talleres_gusto2_ids.unlink()
 #
#          # Paso 2: Crear los registros relacionados en el campo One2many
#            for taller in record.talleres_gusto_ids:
#                self.env['gusto.talleres'].create({
#                    'name': taller.name,  # Copiar el nombre del taller
#                    'gusto_id': record.id,  # Establecer la relación inversa
#                })
    ###############################################################

    
    """
    def write(self, vals):
        # Verificamos si alguno de los campos STO ha cambiado
        pasa = False
        
        if 'name' in vals or 'provincia' in vals or  'participante' in vals or 'pt_nombre' in vals:
            pasa = True           
        if 'pt_apellido1' in vals or 'pt_apellido2' in vals or 'unidad' in vals or 'alta_sto' in vals:
            pasa = True           
        if 'baja_sto' in vals or 'colectivo' in vals or 'inicio_atencion' in vals or 'fin_atencion' in vals:
            pasa = True            
        if 'h_orienta' in vals or 'h_forma' in vals or 'recibi' in vals or 'inicio_inserccion' in vals:
             pasa = True
        if 'fin_inserccion' in vals or 'h_fase_inserccion' in vals or 'd_fase_inserccion' in vals: 
             pasa = True
        if pasa:
            # Creamos un registro en modeloB con los valores actualizados
            self.env['gusto.historico.sto'].create({
                'name': vals.get('name', self.name),  # Usa el valor actualizado o el valor actual
                'provincia': vals.get('provincia', self.provincia),
                'participante': vals.get('participante', self.participante),
                'pt_nombre': vals.get('pt_nombre', self.pt_nombre),  # Usa el valor actualizado o el valor actual

                'pt_apellido1': vals.get('pt_apellido1', self.pt_apellido1),
                'pt_apellido2': vals.get('pt_apellido2', self.pt_apellido2),
                'unidad': vals.get('unidad', self.unidad),  # Usa el valor actualizado o el valor actual
                'alta_sto': vals.get('alta_sto', self.alta_sto),

                'baja_sto': vals.get('baja_sto', self.baja_sto),
                'colectivo': vals.get('colectivo', self.colectivo),  # Usa el valor actualizado o el valor actual
                'inicio_atencion': vals.get('inicio_atencion', self.inicio_atencion),
                'fin_atencion': vals.get('fin_atencion', self.fin_atencion),

                'h_orienta': vals.get('h_orienta', self.h_orienta),  # Usa el valor actualizado o el valor actual
                'h_forma': vals.get('h_forma', self.h_forma),
                'recibi': vals.get('recibi', self.recibi),
                'name': vals.get('name', self.name),  # Usa el valor actualizado o el valor actual
                'inicio_inserccion': vals.get('inicio_inserccion', self.inicio_inserccion),
                'fin_inserccion': vals.get('fin_inserccion', self.fin_inserccion),
                'h_fase_inserccion': vals.get('h_fase_inserccion', self.h_fase_inserccion),
                'd_fase_inserccion': vals.get('d_fase_inserccion', self.d_fase_inserccion),
                'fecha_valor': vals.get('fecha_valor', self.fecha_valor),
            })
        # Llamar al método `write` original para asegurarnos de que se actualicen los registros
        return super(GustoGusto, self).write(vals)
    """
    #@api.onchange('trigger_on_form_load' ) #Esto no esta funcionando y hay que quitarlo de aquí
    @api.onchange('alta_sto', 'baja_sto', 'contratos_ids','contratos_ids.modalidad.name', 
    'contratos_ids.fecha_inicio','contratos_ids.fecha_fin', 'diascomputable', 
    'h_fase_inserccion', 'h_forma', 'h_orienta', 'peonadasc',  'recibi' )
    def _compute_estadisticas(self):
        for rec in self:
            """ 0-PARTICIPANTES STO: Total de participantes registrados en STO con independencia de su  estado """
            if rec.alta_sto:
                rec.q_participante = 1
                rec.q_participanter = 1

            ##########################
            """ 1-BAJA STO: Total de participantes registrados en STO con fecha de baja informada """
            if rec.baja_sto:
                rec.q_baja=1
            else:
                rec.q_baja=0

            ##########################
            """ 2-ORIENTACIÓN: Total de participantes con 10 o más horas de talleres o sesiones 
                               de Orientación Inicial """
            if rec.h_orienta and int(rec.h_orienta.split('h')[0]) >= 10:
                rec.q_orientacion = 1
            else:
                rec.q_orientacion = 0

            ##########################
            """ 3-PERSONA ATENDIDA: Persona Atendida: Total de participantes con 10 o más horas de talleres 
                                    o sesiones de Orientacion Inicial y con 50 o mas horas de formación 
                                    (acciones formativas) """
            if rec.q_orientacion and rec.h_forma and int(rec.h_forma.split('h')[0]) >= 50:
                rec.q_persona_atendida = 1
            else: 
                rec.q_persona_atendida = 0

            ####################################
            ##                                ##
            ##      PONER ALARMA              ##
            ##                                ##
            ####################################
            

            ###########################
            """  4-INCENT.PAGADO: Total de participantes con fecha de recibí del incentivo informada, 
                                  cumple 2. orientación y 3.persona atendida """
            if rec.recibi:
                rec.q_incentivo = 1
            else:
                rec.q_incentivo = 0

            ###########################
            """ 5-OI 40H: Total de participantes con 40 o más horas de talleres o sesiones de 
                          Orientación para la Inserción"""
            if rec.h_fase_inserccion and int(rec.h_fase_inserccion.split('h')[0]) >= 40:
                rec.q_oi40h = 1
            else:
                rec.q_oi40h = 0
            
            ##########################
            """  PARA LOS SIGUIENTE DATOS ESTADISTICOS ES NECESARIO DIFERENCIAR 
                - SI EL CONTRATO ESTA ABIERTO O CERRADO.....PARA PRIORITARIOS O INSERTADOS
                - EL REGIMEN DEL CONTRATO...................PARA PEONADAS Ó DIAS COMPUTABLE
                    """
            rec.fecha_objetivo = False
            if rec.contratos_ids and len(rec.contratos_ids)>=0:
                

                _logger.info(f"#######################################")
                _logger.info(f"#######################################")
                _logger.info(f"#######################################")
                _logger.info(f"##############   Tiene contrato ")
                _logger.info(f"#######################################")
                _logger.info(f"#######################################")
                _logger.info(f"#######################################")
                # FECHA OBJETIVO y FECHA 
                contratos_ordenados = sorted( rec.contratos_ids,key=lambda contrato: contrato.fecha_inicio)
                _logger.info(f"#############   Tiene contrato: {len(contratos_ordenados)}")
                
                if rec.contratos_ids.modalidad[:1].name != 'Cuenta ajena (régimen agrario)':
                    _logger.info(f"#######################################")
                    _logger.info(f"#######################################")
                    _logger.info(f"#######################################")
                    _logger.info(f"##############   Tiene contrato ABIERTO")
                    _logger.info(f"#######################################")
                    _logger.info(f"#######################################")
                    _logger.info(f"#######################################")
                    # REGIMEN GENERAL O AUTONOMO
                    _logger.info(f"Es del regimen GENERAL O AUTONOMO")
                    if any(not contrato.fecha_fin for contrato in rec.contratos_ids):   # SI HAY CONTRATO ESTA ABIERTO
                        contrato_abierto = rec.contratos_ids.filtered(lambda c: not c.fecha_fin)
                        if rec.diascomputable < 120:
                            _logger.info(f"#######################################")
                            _logger.info(f"#######################################")
                            _logger.info(f"#######################################")
                            _logger.info(f"##############   CONTRATO ABIERTO")
                            _logger.info(f"#######################################")
                            _logger.info(f"#######################################")
                            _logger.info(f"#######################################")
                            #if rec.tipo_contratoss not in ('500', '501','502','504','506','507','507','508','510','511','513','518','520','521','530','540','541','550','552'):  
                            rec.q_insertados = 1
                            rec.qt_insertados = 1
                            rec.q_prioritarios = 0 # SI ES INSERTADO NO PUEDE SER PRIORITARIO
                            rec.qt_prioritarios = 0
                              

                            rec.fecha_objetivo = contrato_abierto.fecha_inicio + timedelta(days=120)
                            if fields.Date.today() > rec.fecha_objetivo:
                                rec.fecha_real = contrato_abierto.fecha_inicio + timedelta(days=120)

                            #rec.fecha_objetivo = contrato_abierto.fecha_inicio + timedelta(days=(120 - rec.diascomputable)/(contrato_abierto.porcentaje_jornada/100) )
                        else:
                            rec.q_insertados = 0 # YA ES OSI
                            rec.q_prioritarios = 0  # YA ES OSI
                            rec.qt_prioritarios = 0
                            rec.qt_insertados = 0

                            if rec.q_oi40h:   
                                rec.q_isoconoi = 1
                                rec.q_isosinoi = 0
                            else:
                                rec.q_isoconoi = 0
                                rec.q_isosinoi = 1
                        ## CALCULO DE FECHA OBJETIVA PARA CONTRATOS ABIERTOS
                        # Se tiene en cuenta si la fecha ya ha sido cumplida
                        today = fields.Date.today()
                        
                        diferencia = (119- rec.diascomputable)
                        rec.fecha_objetivo = today + timedelta(days=diferencia)
                        if today > rec.fecha_objetivo:
                            rec.fecha_real = today + timedelta(days=diferencia)

                    else:  # EL CONTRATO ESTA CERRADO
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        _logger.info(f"##############   CONTRATO CERRADO      ")
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                    
                        if rec.diascomputable > 30 and rec.diascomputable < 120:
                            rec.q_prioritarios = 1 
                            rec.q_insertados = 0 # SI ES PRIORITARIO NO PUEDE SER INSERTADO
                            rec.qt_prioritarios = 1
                            rec.qt_insertados = 0

                        else:
                            if rec.q_oi40h:
                                rec.q_isoconoi = 1
                                rec.q_isosinoi = 0
                                rec.q_insertados = 0 # YA ES OSI
                                rec.q_prioritarios = 0  # YA ES OSI
                                rec.qt_prioritarios = 0
                                rec.qt_insertados = 0
                            else:
                                rec.q_isoconoi = 0
                                rec.q_isosinoi = 1
                                rec.q_insertados = 0 # YA ES OSI
                                rec.q_prioritarios = 0  # YA ES OSI
                                rec.qt_prioritarios = 0
                                rec.qt_insertados = 0
                        ## CALCULO DE FECHA OBJETIVA PARA CONTRATOS CERRADOS
                        # Se tiene en cuenta si la fecha ya ha sido cumplida
                        today = fields.Date.today()
                        
                        diferencia = (119 - rec.diascomputable)
                        rec.fecha_objetivo = today + timedelta(days=diferencia)
                        if today > rec.fecha_objetivo:
                            rec.fecha_real = today + timedelta(days=diferencia)




                else:  # 
                    # REGIMEN AGRARIO
                    if any(not contrato.fecha_fin for contrato in rec.contratos_ids):   # SI EL CONTRATO ESTA ABIERTO
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        _logger.info(f"##############   AGRARIO ABIERTO      ")
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        if rec.peonadasc > 0 and rec.peonadasc < 54:
                            rec.q_insertados = 1
                            rec.q_prioritarios = 0 # SI ES INSERTADO NO PUEDE SER PRIORITARIO
                            rec.qt_prioritarios = 0
                            rec.qt_insertados = 1
                        else:
                            rec.q_insertados = 0 # YA ES OSI
                            rec.q_prioritarios = 0  # YA ES OSI
                            if rec.q_oi40h:
                                rec.q_isoconoi = 1
                                rec.q_isosinoi = 0
                                rec.q_insertados = 0 # YA ES OSI
                                rec.q_prioritarios = 0  # YA ES OSI
                                rec.qt_prioritarios = 0
                                rec.qt_insertados = 0
                            else:
                                rec.q_isoconoi = 0
                                rec.q_isosinoi = 1
                                rec.q_insertados = 0 # YA ES OSI
                                rec.q_prioritarios = 0  # YA ES OSI
                                rec.qt_prioritarios = 0
                                rec.qt_insertados = 0
                    else: # CONTRATO CERRADOÇ

                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        _logger.info(f"##############   AGRARIO CERRADO      ")
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        _logger.info(f"#######################################")
                        if rec.peonadasc < 54:
                            rec.q_prioritarios = 1
                            rec.q_insertados = 0
                            rec.qt_prioritarios = 1
                            rec.qt_insertados = 0
                        else:
                            if rec.q_oi40h:
                                rec.q_isoconoi = 1
                                rec.q_isosinoi = 0
                                rec.q_insertados = 0 # YA ES OSI
                                rec.q_prioritarios = 0  # YA ES OSI
                                rec.qt_prioritarios = 0
                                rec.qt_insertados = 0
                            else:
                                rec.q_isoconoi = 0
                                rec.q_isosinoi = 1
                                rec.q_insertados = 0 # YA ES OSI
                                rec.q_prioritarios = 0  # YA ES OSI
                                rec.qt_prioritarios = 0
                                rec.qt_insertados = 0
                    
                    ## CALCULO DE FECHA OBJETIVA PARA CONTRATOS 
                    # Se tiene en cuenta si la fecha ya ha sido cumplida
                    #today = fields.Date.today()
                    #diferencia = (90-(contrato_abierto.fecha_inicio - today).days + rec.peonadasc)
                    #rec.fecha_objetivo = rec.fecha_inicio + timedelta(days=diferencia)
                    rec.fecha_objetivo = False  
            else:
                rec.q_insertados = 0 
                rec.q_prioritarios = 0  
                rec.qt_prioritarios = 0
                rec.qt_insertados = 0
                rec.q_isoconoi = 0
                rec.q_isosinoi = 0

            if rec.fecha_objetivo and rec.fecha_objetivo > fields.Date.today():
                rec.q_participantef = 1
                rec.q_participanter = 0
                rec.fecha_real = False
            
                



    @api.depends('h_orienta', 'h_forma', 'h_fase_inserccion','recibi')
    #def _compute_est_orientacion(self):
    def _compute_estados(self):
        for record in self:
            #  ESTADO DE ORIENTACION
            if record.h_orienta == '00h:00m':
                record.est_orientacion = 'noinciada'
                record.fase_orienta = 'NO INICIADA'
            elif record.h_orienta and int(record.h_orienta.split('h')[0]) >= 10:
                record.est_orientacion = 'finalizada'
                record.fase_orienta = 'FINALIZADA'
            else:
                record.est_orientacion = 'encurso'
                record.fase_orienta = 'EN CURSO'
            #  ESTADO DE FORMACION
            if record.h_forma == '00h:00m':
                record.est_formacion = 'noinciada'
            elif record.h_forma and int(record.h_forma.split('h')[0]) >= 50:
                record.est_formacion = 'finalizada'
            else:
                record.est_formacion = 'encurso'
            #  ESTADO DE INSERCCION
            if record.h_fase_inserccion == '00h:00m':
                record.est_orientacion40 = 'noinciada' 
            elif record.h_fase_inserccion and int(record.h_fase_inserccion.split('h')[0]) >= 40:
                record.est_orientacion40 = 'finalizada'
            else:
                record.est_orientacion40 = 'encurso'
            #  ESTADO DE INSERCCION
            if record.recibi:
                record.est_incentivo = 'si' 
            else:
                record.est_incentivo = 'no'


    @api.depends('contratos_ids')
    def _compute_sum_dias(self):
        for rec in self:
            totdiastrab = 0
            totdiascomp = 0
            totpeonadasc = 0
            if rec.contratos_ids:
                totdiastrab = sum(contrato.diastrabajado for contrato in rec.contratos_ids)
                rec.diastrabajado = totdiastrab 

                for contrato in rec.contratos_ids:
                    #totdiastrab += contrato.diastrabajado
                    if contrato.modalidad.name != 'Cuenta ajena (régimen agrario)':
                        totdiascomp += contrato.diascomputable
                        rec.es_agrario = False
                    else:
                        totpeonadasc += contrato.peonadas
                        rec.es_agrario = True
                    
                    if contrato.jornada.name == 'Jornada completa':
                        rec.es_parcial = True
                    else:
                        rec.es_parcial = False

                rec.diastrabajado = totdiastrab
                rec.diascomputable = totdiascomp
                rec.peonadasc = totpeonadasc

            
    
    
    #@api.depends('contratos_ids.diastrabajado')
    #def _compute_sum_dias_trabajado(self):
    #    """Función para sumar los días trabajados de todos los contratos asociados"""
    #    for rec in self:
    #        totdiastrab = sum(contrato.diastrabajado for contrato in rec.contratos_ids)
    #        rec.diastrabajado = totdiastrab
                            

    #@api.depends('contratos_ids.diascomputable')
    #def _compute_sum_dias_computado(self):
    #    """Función para sumar los días trabajados de todos los contratos asociados"""
    #    for rec in self:
    #        totdiascomp = sum(contrato.diascomputable for contrato in rec.contratos_ids)
    #        rec.diascomputable = totdiascomp

    #        if rec.contratos_ids:
    #            rec.peonadasc = rec.contratos_ids[0].peonadasc
    #        else:
    #            rec.peonadasc = 0
####
####
    @api.depends('talleres_gusto_ids')
    def _cargando_talleres(self):
        for rec in records:
            # Vaciar los datos existentes en el campo talleres_gusto2_ids
            rec.talleres_gusto2_ids.unlink()
            
            lines = []
            
            
            # Obtener los registros relacionados desde gusto_talleres1_rel usando ORM
            records_ta = env['gusto.talleres1.rel'].search([('gusto_gusto_id', '=', rec.id)])
            #if records_ta:
            #    for s in records_ta:
            #        vals = (0,0, {'talleres_id': s.gusto_talleres_id})
            #        lines.append(vals)
                
            #    rec.talleres_gusto2_ids = lines



    @api.onchange('talleres_gusto_ids')
    def _compute_horas_gusto(self):
        for record in self:
            # Inicializa las sumas en cero
            h_orienta = 0
            h_ori_ins = 0
            h_anexo = 0
            h_anexo3 = 200

            # Recorre cada registro en talleres_gusto_ids
            for taller in record.talleres_gusto_ids:
                h_anexo3 = 100
                if taller.tipo_gusto and taller.tipo_gusto.name == 'ORIENTACION INICIAL':
                    h_orienta += taller.horas
                    h_anexo3 += 1
                elif taller.tipo_gusto and taller.tipo_gusto.name == 'ORIENTACION PARA LA INSERCCIÓN':
                    h_ori_ins += taller.horas
                    h_anexo3 += 1
                elif taller.tipo_gusto and taller.tipo_gusto.name == 'ANEXO A LA PARTICIPACION':
                    h_anexo += taller.horas
                    h_anexo3 += 1

            # Asigna las sumas a los campos correspondientes
            record.h_orienta_gus = h_orienta
            record.h_ori_ins_gus = h_ori_ins
            record.h_anexo_gus = h_anexo
            record.h_anexo3_gus = h_anexo3

    # Botón para abrir el popup de creación de talleres
    #def action_open_create_taller(self):
    #    return {
    #        'name': 'Crear Taller1',
    #        'type': 'ir.actions.act_window',
    #        'res_model': 'gusto.talleres',
    #        'view_mode': 'form',
    #        'target': 'new',  # Indica que el formulario se abre en un popup
    #        'context': {
    #            'default_provincia_id': self._get_provincia_id(),
    #            'default_modalidad': 'individual',
    #            'default_gusto_id': self.id,  # Asocia el taller al registro actual
    #        }
    #    }

    def action_open_create_taller(self):
        view_id = self.env.ref('gusto.view_form_gusto_talleres_creation').id
        return {
            'name': 'Crear Taller Indiviual',
            'type': 'ir.actions.act_window',
            'res_model': 'gusto.talleres',
            'view_mode': 'form',
            'view_id': view_id,  # Especificar la vista
            'target': 'current',  # Indica que el formulario se abre en un popup
            'context': {
                'default_provincia_id': self._get_provincia_id(),
                'default_modalidad': 'individual',
                'default_gusto_id': self.id,  # Asocia el taller al registro actual
                'default_pt_nombre': self.pt_nombre,
                'default_pt_apellido1': self.pt_apellido1,
                'default_pt_apellido2': self.pt_apellido2,
            }
        }

    # Método para actualizar talleres_gusto_ids después de la creación
    @api.model
    def create_taller_and_update(self, gusto_id, taller_id):
        """
        Actualiza los campos relacionados entre gusto.gusto y gusto.talleres.
        """
        _logger.info(f"Iniciando actualización para gusto_id: {gusto_id}, taller_id: {taller_id}")
        
        gusto = self.browse(gusto_id)
        if gusto:
            _logger.info(f"Talleres antes de actualizar en gusto.gusto: {gusto.talleres_gusto_ids.ids}")
            gusto.write({'talleres_gusto_ids': [(4, taller_id)]})
            _logger.info(f"Talleres después de actualizar en gusto.gusto: {gusto.talleres_gusto_ids.ids}")
            
            # Vincular el participante en el taller
            taller = self.env['gusto.talleres'].browse(taller_id)
            if taller:
                _logger.info(f"Participantes antes de actualizar en gusto.talleres: {taller.participantes_talleres_ids.ids}")
                taller.write({'participantes_talleres_ids': [(4, gusto_id)]})
                _logger.info(f"Participantes después de actualizar en gusto.talleres: {taller.participantes_talleres_ids.ids}")


    # Crear un taller individual
    def action_open_taller_creation_form(self):
        """Abre un formulario para crear un nuevo registro en gusto.talleres."""
        view_id = self.env.ref('gusto.view_form_gusto_talleres_creation').id
        self.pasap = False
        return {
            'type': 'ir.actions.act_window',
            'name': 'Crear Taller2',
            'res_model': 'gusto.talleres',
            'view_mode': 'form',
            'view_id': view_id,  # Especificar la vista
            'target': 'new',
            'context': {
                'default_provincia_id': self._get_provincia_id(),
                'default_gusto_id': self.id,
                'default_modalidad': 'individual',
                'default_pt_nombre': self.pt_nombre,
                'default_pt_apellido1': self.pt_apellido1,
                'default_pt_apellido2': self.pt_apellido2,
                #'default_tipo_gusto_domain': [('name', 'ilike', 'individual')],
                'create_taller_callback': self._create_taller_callback,
            },
        }
    # Crear contrato 
    def action_open_contrato_creation_form(self):
        """Abre un formulario para crear un nuevo registro en gusto.contratos."""
        view_id = self.env.ref('gusto.view_form_gusto_contratos_creation').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Crear Contrato',
            'res_model': 'gusto.contratos',
            'view_mode': 'form',
            'view_id': view_id,  # Especificar la vista
            'target': 'new',
            'context': {
                'default_participante_id': self.id,
            },
        }

    def _create_taller_callback(self, result):
        """Callback que se ejecuta después de crear un taller para asignar el valor a pasap."""
        _logger.info(f"Callback recibido con resultado: {result}")
        self.pasap = result.get('id', False)
        _logger.info(f"$$$$$$   OOOOOO   $$$$$$$$$$$    El ID del gusto es: {self.id} el del taller es: {self.pasap}")
        return True
    
    def _get_provincia_id(self):
        """Busca la provincia_id correspondiente al nombre en gusto.gusto."""
        state = self.env['res.country.state'].search([('name', 'ilike', self.provincia)], limit=1)
        return state.id if state else False

    @api.model
    def add_to_talleres_gusto(self, gusto_id, taller_id):
        """
        Actualiza el campo Many2many para vincular un gusto con un taller.
        """
        gusto = self.env['gusto.gusto'].browse(gusto_id)
        taller = self.env['gusto.talleres'].browse(taller_id)

        if gusto and taller:
            gusto.write({'talleres_gusto_ids': [(4, taller_id)]})
            taller.write({'participantes_talleres_ids': [(4, gusto_id)]})
            _logger.info(f"Vinculado gusto_id {gusto_id} con talleres_id {taller_id} usando Many2many")


    @api.model
    def obtener_informe_provincia(self):
        query = """
            SELECT provincia,
                   COUNT(*) as total,
                   SUM(CASE WHEN fase_orienta = 'FINALIZADA' THEN 1 ELSE 0 END) as orientacion_finalizada,
                   SUM(CASE WHEN fase_orienta = 'FINALIZADA' AND est_formacion = 'finalizada' THEN 1 ELSE 0 END) as formacion_finalizada
            FROM gusto_gusto
            GROUP BY provincia
        """
        self.env.cr.execute(query)
        resultados = self.env.cr.dictfetchall()
        return resultados        
    
