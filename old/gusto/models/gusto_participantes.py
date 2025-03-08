
from odoo import models, fields, api


class GustoParticipantes(models.Model):
    #_name = 'crm_gusto.participantes'
    _description = 'Registro de participantes'
    _inherit = 'res.partner'


    es_gusto_participante = fields.Boolean('SOLICITANTE', default=False) 
    
    # correo, telefono, dni vienen heredados de rest.partner
    # name se computa de los tres siguientes
    name = fields.Char(compute='_compute_name', store = True)
    nombre = fields.Char('DENOMINACION')          
    apellido1 = fields.Char('PRIMER APELLIDO')
    apellido2 = fields.Char('SEGUNDO APELLIDO')
    

    #### PROYCEN GENERAL
    asunto = fields.Char('ASUNTO')
    mensaje = fields.Text('MENSAJE')
    
    #### AE+ GENERAL
    interes_profesionales = fields.Many2many('gusto.interesprofesionales', string='INTERESES PROFESIONALES')



    ##### PROYCEN INTEGRALES
    genero = fields.Selection([('masculino','MASCULINO'),('femenino','FEMENINO'),('prefierono','PREFIERO NO ESPECIFICAR'),('otro','OTRO')])
    fecha_nacimiento = fields.Date('FECHA NACIMIENTO')
    situacion_laboral = fields.Selection([('empleado','EMPLEADO/A'),
                                          ('atutonomo','AUTÓNOMO'),
                                          ('contratado','CONTRATADO/A TEMPORALMENTE'),
                                          ('desempleado','DESEMPLEADO'),
                                          ('estudiente','ESTUDIANTE'),
                                          ('otra','OTRA SITUACIÓN'),])
    otra_situacion_laboral = fields.Char()
    garantia_juvenil = fields.Boolean('GARANTIA JUVENIL')
    nivel_estudio = fields.Selection([('sinestudios','SIN ESTUDIOS'),
                                          ('primaria','EDUCACIÓN PRIMARIA'),
                                          ('secundaria','EDUCACIÓN SECUNDARIA O EQUIVALENTE'),
                                          ('formacionprofesional','FORMACION PROFESIONAL'),
                                          ('bachillerato','BACHILLERATO O EQUIVALENTE'),
                                          ('grado','GRADO UNIVERSITARIO O LICENCIATURA'),
                                          ('postgrado','ESPECIALIZACIÓN O DIPLOMADO'),
                                          ('maestria','MAESTRÍA O MÁSTER'),
                                          ('doctorado','DOCTORADO (Ph D)'),
                                          ('otro','OTROS ESTUCDIOS NO FORMALES'),])
    otros_nivel_estudio = fields.Char()

    experiencia_laboral = fields.Many2many('gusto.experiencialaboral', string='EXPERIENCIA LABORAL')

    objetivo_profesional = fields.Many2many('gusto.objetivoprofesional', string='OBJETIVO PROFESIONAL')
    otro_objetivo_profesional = fields.Char()
    necesidades_formacion_especifica = fields.Many2many('gusto.necesidadesformacionespecifica', string='NECESIDADES FORMACION ESPECIFICA')
    otras_necesidades_formacion_especifica = fields.Char('OTRAS NECESIDADES FORMACION ESPECIFICA')
    #intereses_profesionales = fields.Many2many('gusto.interesesprofesionales', string='INTERESES PROFESIONALES')  


    #### NECESARIOS
    procedencia_entrada = fields.Many2one ('gusto.procedenciaentrada', 'PROCEDENCIA')

    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company)

    
    estado = fields.Selection([('sinrevisar','SIN REVISAR'), 
                               ('asignado','ASIGNADO A TECNICO'),
                               ('descartado','DESCARTADO'),
                               ('pendiente','PENDIENTE'),
                               ('programa','EN PROGRAMA')])
    observaciones = fields.Char('Observaciones')

    proyectos_ids = fields.Many2many('gusto.proyectos', relation='gusto_participantes_proyectos_rel',string='PROYECTOS')
    programas_ids = fields.Many2many('gusto.programas', relation='gusto_participantes_programas_rel',string='PROGRAMAS')
    convocatoria_sol_id = fields.Many2one('gusto.convocatoria', string='SOLICITUD DE CONVOCATORIA')
    #convocatoria_par_id = fields.Many2one('gusto.convocatoria', string='CONVOCATORIA DEL PARTICIPANTE')




    