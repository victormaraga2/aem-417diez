
from odoo import models, fields, api


class CaptacionSolicitudes(models.Model):
    #_name = 'crm_captacion.participantes'
    _description = 'Registro de solicitudes'
    _inherit = 'crm.lead'

    
    nombre = fields.Char('NOMBRE')     
    apellidos = fields.Char('APELLIDOS')          
    
   
    situacion_laboral = fields.Selection([('empleado','EMPLEADO/A'),
                                          ('autonomo','AUTÓNOMO'),
                                          ('contratado','CONTRATADO/A TEMPORALMENTE'),
                                          ('desempleado','DESEMPLEADO'),
                                          ('estudiente','ESTUDIANTE'),
                                          ('otra','OTRA SITUACIÓN'),])
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


    procedencia_entrada = fields.Many2one ('captacion.procedenciaentrada', 'PROCEDENCIA')
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")


    #convocatoria_sol_id = fields.Many2one('captacion.convocatoria', string='CONVOCATORIA')
    #convocatoria_par_id = fields.Many2one('captacion.convocatoria', string='CONVOCATORIA')
   
    




    