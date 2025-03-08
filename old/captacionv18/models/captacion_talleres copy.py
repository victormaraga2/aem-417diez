from odoo import models, fields, api, _
import re
from datetime import timedelta
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)




class CaptacionTalleress(models.Model):
    _name = 'captacion.talleres'
    _description = 'Registro de talleres'

    id = fields.Integer(string='ID')
    #######################################################################################################
    #
    #    CARGA DEL STO
    #
    #######################################################################################################
    id_sto = fields.Integer('ID_STO')
    country_id = fields.Many2one('res.country', string='País', default=lambda self: self.env.ref('base.es'))
    provincia_id = fields.Many2one('res.country.state',  
                                   domain="[('country_id', '=', country_id), ('name', 'in', ['Cádiz', 'Córdoba', 'Granada', 'Huelva', 'Jaén', 'Málaga', 'Sevilla', 'Almería'])]",
                                   string='PROVINCIA')
    
    ### Campos añadidos por Victor ### 14/01/2025
    ####################################################
    pt_nombre=fields.Char('PT. NOMBRE')                    #   STO -> PT. NOMBRE
    pt_apellido1=fields.Char('PT. APELLIDO1')              #   STO -> PT. APELLIDO1
    pt_apellido2=fields.Char('PT. APELLIDO2')              #   STO -> PT. APELLIDO1

    # provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company    
    #####################################################

    name = fields.Char('DENOMINACION')    
    #tipo_ori = fields.Char('TIPO ORIENTACION')
    fec_inicio = fields.Date('F. INICIO')
    fec_fin = fields.Date('F. FIN')
    horas = fields.Float('HORAS')
    turno = fields.Char('TURNO MÑN-TARDE')
    aula = fields.Char('AULA')
    pt_nombre = fields.Char('NOMBRE')
    pt_apellido1 = fields.Char('APELLIDO1')
    pt_apellido2 = fields.Char('APELLIDO2')
    unidad = fields.Char('UNIDAD')
    tipo = fields.Many2one('captacion.tipo.formacion','TIPO STO')
    tipo_captacion = fields.Many2one('captacion.tipo.doc','TIPO CAPTACION')
    

    estado = fields.Char('ESTADO')



    ######################################################################################################
    #
    #               NECESARIOS PARA CAPTACION
    #
    ######################################################################################################


    # modalidad = fields.Selection([('individual', 'Individual'), ('grupal', 'Grupal')])
    modalidad = fields.Selection([('individual', 'Individual'), ('grupal', 'Grupal')], default='grupal', required=True, string='MODALIDAD')
    observaciones = fields.Char('Observaciones')
    docaem_ids = fields.One2many('captacion.docaem', 'taller_id', string='DOCUMENTACION')
    
    participantes_talleres_ids = fields.Many2many('res.partner', relation='captacion_talleres1_rel', string='PARTICIPANTES')
    participantes_talleres2_ids = fields.One2many('res.partner', 'talleres_id')
    captacion_id = fields.Many2one('res.partner', string='PARTICIPANTES') # Necesario para captacion
    captacion_name = fields.Char( related='captacion_id.participante') 
    captacion_id_id = fields.Integer (related='captacion_id.id')
    
 

    @api.onchange('participantes_talleres_ids')
    def onchange_participantes(self):
        """Lógica para manejar el cambio de participantes_talleres_ids."""
        if self.modalidad != 'individual' and self.participantes_talleres_ids:
            self.create_docaem_grupal_records()            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'captacion.confirm.docaem.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_talleres_id': self.id,
                }
            }
        
    def action_view_documents(self):
        return {
            'name': 'Documentos Relacionados',
            'type': 'ir.actions.act_window',
            'res_model': 'captacion.docaem',
            'view_mode': 'form',
            'domain': [('taller_id', '=', self.id), ('captacion_id', '=', self.captacion_id.name)],
            'context': {'default_taller_id': self.id, 'default_captacion_id': self.captacion_id.name},
            'res_id': self.id,  # Abre el archivo del registro actual
            'views': [(self.env.ref('captacion.view_file_viewer_form').id, 'form')],
            'target': 'new',  # Abrir en un popup
        }
    
    def action_open_file_viewer(self):
        # Devuelve la vista del archivo en un formulario popup
        return {
            'name': 'Visor de Archivo',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'captacion.docaem',
            'domain': [('taller_id', '=', self.id), ('captacion_id', '=', self.captacion_id.id)],
            'context': {'default_taller_id': self.id, 'default_captacion_id': self.captacion_id.id},
            'res_id': self.id,  # Abre el archivo del registro actual
            'views': [(self.env.ref('captacion.view_file_viewer_form').id, 'form')],
            'target': 'new',  # Abrir en un popup
        }
    
    
    #@api.model
    #def default_get(self, fields):
    #    """Ajustar el dominio dinámicamente según el contexto."""
    #    res = super(CaptacionTalleress, self).default_get(fields)
    #    if self.env.context.get('default_modalidad') == 'individual':
    #        # Caso creación desde res.partner: Permitir solo 'INDIVIDUAL'
    #        res['tipo_captacion_domain'] = [('name', 'ilike', 'INDIVIDUAL')]
    #    else:
    #        # Caso creación directa desde captacion.talleres: Excluir 'INDIVIDUAL'
    #        res['tipo_captacion_domain'] = [('name', 'not ilike', 'INDIVIDUAL')]
    #    return res

    @api.onchange('tipo_captacion')
    def _onchange_tipo_captacion(self):
        """Validar que el valor de tipo_captacion cumpla con el dominio."""
        if self.tipo_captacion:
            domain = self.env.context.get('tipo_captacion_domain')
            if domain and not self.tipo_captacion.name in [d[2] for d in domain if 'name' in d]:
                self.tipo_captacion = False
                return {
                    'warning': {
                        'title': 'Selección inválida',
                        'message': 'El valor seleccionado no está permitido para este contexto.',
                    }
                }
    
    @api.model
    def create(self, vals):
        
        modalidad = self.env.context.get('default_modalidad')

        if not modalidad:
            modalidad = vals.get('modalidad')
        
        captacion_id = self.env.context.get('default_captacion_id')

        # Validar modalidad
        #if not modalidad:
        #    raise ValidationError(f"La modalidad no está definida en el contexto.{vals}")

        #if not isinstance(vals, dict):
        #    raise ValidationError(f"Los valores proporcionados no son válidos.'{vals}'")
        
        
        if modalidad == 'individual':

            if isinstance(vals, dict):

                _logger.info(f"Creando taller con modalidad '{modalidad}' y captacion_id '{captacion_id}'. Valores: {vals}")
            
                # Crear taller según la modalidad
                taller = super(CaptacionTalleress, self).create(vals)


                if not captacion_id:
                    raise ValidationError("El 'captacion_id' es obligatorio para la modalidad individual.")
                
                _logger.info(f"Relacionando captacion_id con el taller '{modalidad}' y captacion_id '{captacion_id}'. Valores: {vals}")
                # Relacionar el captacion_id con el taller
                taller.write({'participantes_talleres_ids': [(4, int(captacion_id))]})
                
                # Crear registros individuales en captacion.docaem
                taller.create_docaem_individual_records()
            
            else:
                raise ValidationError(f"Los valores proporcionados no son válidos.'{vals}'")

            return taller   
        """
        elif modalidad == 'grupal':

            _logger.info(f"Creando taller con modalidad '{modalidad}' y captacion_id '{captacion_id}'. Valores: {vals}")
            
            # Crear taller según la modalidad
            taller = super(CaptacionTalleress, self).create(vals)
            
            command = vals['participantes_talleres_ids'][0]
            participantes_ids = command[2]

            _logger.info(f"IDs de participantes: {participantes_ids}")
            for participante in participantes_ids:
                taller.write({'participantes_talleres_ids': [(4, participante)]})

            taller.create_docaem_grupal_records()
            return taller
        """    

   
    def create_docaem_individual_records(self):
        """Crear registros en captacion.docaem según la duración del taller."""
        for record in self:
            if record.fec_inicio and record.fec_fin and record.captacion_id:
                rango_dias = (record.fec_fin - record.fec_inicio).days + 1
                fechas = [record.fec_inicio + timedelta(days=i) for i in range(rango_dias)]

                # Filtrar solo los días laborables (lunes a viernes)
                dias_laborables = [fecha for fecha in fechas if fecha.weekday() not in (5, 6)]  # Excluir sábados y domingos

                # Calcular las horas por día según los días laborables
                rango_dias_laborables = len(dias_laborables)
                horas_por_dia = record.horas / rango_dias_laborables if rango_dias_laborables > 0 else 0

                for fecha in fechas:
                    # Excluir sábados (5) y domingos (6)
                    if fecha.weekday() in (5, 6):  # 5: Sábado, 6: Domingo
                        _logger.info(f"Excluyendo fecha '{fecha}' porque es fin de semana.")
                        continue
                    self.env['captacion.docaem'].create({
                        'taller_id': record.id,
                        'fecha': fecha,
                        'horas': horas_por_dia,
                        'captacion_id': record.captacion_id.id,
                        'tipo_doc_id': record.tipo_captacion.id,
                        'name': f"{record.captacion_id.name} - {fecha}"
                    })
                    _logger.info(f"Creando documento para taller '{record.id}' y fecha '{fecha}' y captacion_id '{record.captacion_id.id}'.")
    

    def create_docaem_grupal_records(self):
        """Crear registros en captacion.docaem para talleres grupales."""
        for record in self:
            if record.fec_inicio and record.fec_fin and record.participantes_talleres_ids:
                rango_dias = (record.fec_fin - record.fec_inicio).days + 1
                fechas = [record.fec_inicio + timedelta(days=i) for i in range(rango_dias)]

                # Filtrar solo los días laborables (lunes a viernes)
                dias_laborables = [fecha for fecha in fechas if fecha.weekday() not in (5, 6)]  # Excluir sábados y domingos

                # Calcular las horas por día según los días laborables
                rango_dias_laborables = len(dias_laborables)
                horas_por_dia = record.horas / rango_dias_laborables if rango_dias_laborables > 0 else 0
    
                for participante in record.participantes_talleres_ids:
                    # Añadir el taller al participante
                    participante.write({'talleres_captacion2_ids': [(4, record.id)]})
                    _logger.info(f"IDs de participante: {participante} , ID_TALLER: {record.id}")
                    for fecha in fechas:
                        # Excluir sábados (5) y domingos (6)
                        if fecha.weekday() in (5, 6):  # 5: Sábado, 6: Domingo
                            _logger.info(f"Excluyendo fecha '{fecha}' porque es fin de semana.")
                            continue
                        
                        
                        # Verificar si ya existe un registro en docaem para este participante, taller y fecha
                        existing_record = self.env['captacion.docaem'].search([
                            ('taller_id', '=', record._origin.id),
                            ('captacion_id', '=', participante._origin.id),
                            ('fecha', '=', fecha),
                        ], limit=1)
                        _logger.info(f"Registros encontrados: {len(existing_record)} para taller_id: {record.id}, captacion_id: {participante.id}, fecha: {fecha}")

                        # Si no existe un registro, crear uno nuevo
                        if not existing_record:
                            self.env['captacion.docaem'].create({
                                'taller_id': record.id,
                                'fecha': fecha,
                                'horas': horas_por_dia,
                                'captacion_id': participante.id,
                                'tipo_doc_id': record.tipo_captacion.id,
                                'name': f"Taller: {record.name} - {participante.participante} - {fecha}",
                                'grupal': True,
                            })
                            _logger.info(f"Documento de taller_id: '{record.id}' captacion_id: '{participante.id}' y fecha: '{fecha}' NO EXISTE y se crea")
                        else:
                            _logger.info(f"Documento de taller_id: '{record.id}' captacion_id: '{participante.id}' y fecha: '{fecha}' EXISTE")
                            
                        """
                        self.env['captacion.docaem'].create({
                            'taller_id': record.id,
                            'fecha': fecha,
                            'horas': horas_por_dia,
                            'captacion_id': participante.id,
                            'tipo_doc_id': record.tipo_captacion.id,
                            'name': f"Taller: {record.name} - {participante.participante} - {fecha}",
                            'grupal': True,
                        })
                        """
                        

     


    """
    @api.model
        def create(self, vals):
            ""
            Sobrescribe el método `create` para manejar tanto diccionarios como enteros y actualizar las relaciones.
            ""
            
            _logger.info(f"#####################   Valores recibidos para crear un taller: {vals} . y tambien el captacion id: {self.captacion_id} ")

            # Si vals es un entero, devolver el registro correspondiente (y evitar llamar a create nuevamente)
            #if isinstance(vals, int):
            #    _logger.warning(f"########################   Se recibió un ID en lugar de un diccionario: {vals}. Retornando el registro existente.")
            #    return self.browse(vals)
            
            # Si vals no es un diccionario, lanzar una excepción
            if not isinstance(vals, dict):
                raise ValidationError(f"#######################   Se esperaba un diccionario, pero se recibió: {type(vals).__name__}")
    #
            # Crear el registro con los valores válidos
            res = super(CaptacionTalleress, self).create(vals)

            # Registrar el ID del nuevo taller
            #_logger.info(f"#######################    Se creó un nuevo taller con ID: {res.id}")


            ##########################  Añadido por Victor 21/01/2025 ####################
            ##############################################################################
            ""
            # Verificar si hay fechas de inicio y fin
            fec_inicio = vals.get('fec_inicio')
            fec_fin = vals.get('fec_fin', fec_inicio)  # Usar la misma fecha si no hay fec_fin

            if fec_inicio:
                # Calcular los días de duración
                fec_inicio = fields.Date.from_string(fec_inicio)
                fec_fin = fields.Date.from_string(fec_fin)
                duracion = (fec_fin - fec_inicio).days + 1  # Incluye ambos días

                # Iterar sobre cada día
                for i in range(duracion):
                    fecha = fec_inicio + timedelta(days=i)

                    # Crear el registro en captacion.docaem
                    self.env['captacion.docaem'].create({
                        'taller_id': res.id,          # ID del taller recién creado
                        # 'tipo_doc_id': res.id_tipo_captacion,
                        'name': f"{res.name} - {fecha}",
                        'fecha': fecha,
                        'horas': res.horas / duracion if duracion > 0 else res.horas,
                    })
            ""
            ##########################################################
            #########################################################
            if 'captacion_id' in vals:
                captacion = self.env['res.partner'].browse(vals['captacion_id'])
                captacion.write({'talleres_captacion_ids': [(4, res.id)]})  # Añadir taller al usuario
                res.write({'participantes_talleres_ids': [(4, captacion.id)]})  # Añadir usuario al taller

            # Crear registros en captacion.docaem
            res.create_docaem_records()

            # Vincular al res.partner si es necesario
            if 'captacion_id' in vals:
                captacion = self.env['res.partner'].browse(vals['captacion_id'])
                _logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$$    El ID del captacion asociado es: {captacion_id}")
                if captacion:
                    _logger.info(f"$$$$$$$$$$$$$$$$$$$$$$   Talleres antes de actualizar en res.partner: {captacion.talleres_captacion_ids.ids}")
                    captacion.write({'talleres_captacion_ids': [(4, res.id)]})
                    _logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$    Talleres después de actualizar en res.partner: {captacion.talleres_captacion_ids.ids}")
    #
                    # Vincular el participante en el taller
                    _logger.info(f"$$$$$$$$$$$$$$$$$   Participantes antes de actualizar en captacion.talleres: {res.participantes_talleres_ids.ids}")
                    res.write({'participantes_talleres_ids': [(4, captacion.id)]})
                    _logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$   Participantes después de actualizar en captacion.talleres: {res.participantes_talleres_ids.ids}")
    #
            return res
    """