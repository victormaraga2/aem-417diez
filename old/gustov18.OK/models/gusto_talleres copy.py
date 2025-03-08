from odoo import models, fields, api, _
import re
from datetime import timedelta
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)




class GustoTalleress(models.Model):
    _name = 'gusto.talleres'
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
    tipo = fields.Many2one('gusto.tipo.formacion','TIPO STO')
    tipo_gusto = fields.Many2one('gusto.tipo.doc','TIPO GUSTO')
    

    estado = fields.Char('ESTADO')



    ######################################################################################################
    #
    #               NECESARIOS PARA GUSTO
    #
    ######################################################################################################


    # modalidad = fields.Selection([('individual', 'Individual'), ('grupal', 'Grupal')])
    modalidad = fields.Selection([('individual', 'Individual'), ('grupal', 'Grupal')], default='grupal', required=True, string='MODALIDAD')
    observaciones = fields.Char('Observaciones')
    docaem_ids = fields.One2many('gusto.docaem', 'taller_id', string='DOCUMENTACION')
    
    participantes_talleres_ids = fields.Many2many('gusto.gusto', relation='gusto_talleres1_rel', string='PARTICIPANTES')
    participantes_talleres2_ids = fields.One2many('gusto.gusto', 'talleres_id')
    gusto_id = fields.Many2one('gusto.gusto', string='PARTICIPANTES') # Necesario para gusto
    gusto_name = fields.Char( related='gusto_id.participante') 
    gusto_id_id = fields.Integer (related='gusto_id.id')
    
 

    @api.onchange('participantes_talleres_ids')
    def onchange_participantes(self):
        """Lógica para manejar el cambio de participantes_talleres_ids."""
        if self.modalidad != 'individual' and self.participantes_talleres_ids:
            self.create_docaem_grupal_records()            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'gusto.confirm.docaem.wizard',
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
            'res_model': 'gusto.docaem',
            'view_mode': 'form',
            'domain': [('taller_id', '=', self.id), ('gusto_id', '=', self.gusto_id.name)],
            'context': {'default_taller_id': self.id, 'default_gusto_id': self.gusto_id.name},
            'res_id': self.id,  # Abre el archivo del registro actual
            'views': [(self.env.ref('gusto.view_file_viewer_form').id, 'form')],
            'target': 'new',  # Abrir en un popup
        }
    
    def action_open_file_viewer(self):
        # Devuelve la vista del archivo en un formulario popup
        return {
            'name': 'Visor de Archivo',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'gusto.docaem',
            'domain': [('taller_id', '=', self.id), ('gusto_id', '=', self.gusto_id.id)],
            'context': {'default_taller_id': self.id, 'default_gusto_id': self.gusto_id.id},
            'res_id': self.id,  # Abre el archivo del registro actual
            'views': [(self.env.ref('gusto.view_file_viewer_form').id, 'form')],
            'target': 'new',  # Abrir en un popup
        }
    
    
    #@api.model
    #def default_get(self, fields):
    #    """Ajustar el dominio dinámicamente según el contexto."""
    #    res = super(GustoTalleress, self).default_get(fields)
    #    if self.env.context.get('default_modalidad') == 'individual':
    #        # Caso creación desde gusto.gusto: Permitir solo 'INDIVIDUAL'
    #        res['tipo_gusto_domain'] = [('name', 'ilike', 'INDIVIDUAL')]
    #    else:
    #        # Caso creación directa desde gusto.talleres: Excluir 'INDIVIDUAL'
    #        res['tipo_gusto_domain'] = [('name', 'not ilike', 'INDIVIDUAL')]
    #    return res

    @api.onchange('tipo_gusto')
    def _onchange_tipo_gusto(self):
        """Validar que el valor de tipo_gusto cumpla con el dominio."""
        if self.tipo_gusto:
            domain = self.env.context.get('tipo_gusto_domain')
            if domain and not self.tipo_gusto.name in [d[2] for d in domain if 'name' in d]:
                self.tipo_gusto = False
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
        
        gusto_id = self.env.context.get('default_gusto_id')

        # Validar modalidad
        #if not modalidad:
        #    raise ValidationError(f"La modalidad no está definida en el contexto.{vals}")

        #if not isinstance(vals, dict):
        #    raise ValidationError(f"Los valores proporcionados no son válidos.'{vals}'")
        
        
        if modalidad == 'individual':

            if isinstance(vals, dict):

                _logger.info(f"Creando taller con modalidad '{modalidad}' y gusto_id '{gusto_id}'. Valores: {vals}")
            
                # Crear taller según la modalidad
                taller = super(GustoTalleress, self).create(vals)


                if not gusto_id:
                    raise ValidationError("El 'gusto_id' es obligatorio para la modalidad individual.")
                
                _logger.info(f"Relacionando gusto_id con el taller '{modalidad}' y gusto_id '{gusto_id}'. Valores: {vals}")
                # Relacionar el gusto_id con el taller
                taller.write({'participantes_talleres_ids': [(4, int(gusto_id))]})
                
                # Crear registros individuales en gusto.docaem
                taller.create_docaem_individual_records()
            
            else:
                raise ValidationError(f"Los valores proporcionados no son válidos.'{vals}'")

            return taller   
        """
        elif modalidad == 'grupal':

            _logger.info(f"Creando taller con modalidad '{modalidad}' y gusto_id '{gusto_id}'. Valores: {vals}")
            
            # Crear taller según la modalidad
            taller = super(GustoTalleress, self).create(vals)
            
            command = vals['participantes_talleres_ids'][0]
            participantes_ids = command[2]

            _logger.info(f"IDs de participantes: {participantes_ids}")
            for participante in participantes_ids:
                taller.write({'participantes_talleres_ids': [(4, participante)]})

            taller.create_docaem_grupal_records()
            return taller
        """    

   
    def create_docaem_individual_records(self):
        """Crear registros en gusto.docaem según la duración del taller."""
        for record in self:
            if record.fec_inicio and record.fec_fin and record.gusto_id:
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
                    self.env['gusto.docaem'].create({
                        'taller_id': record.id,
                        'fecha': fecha,
                        'horas': horas_por_dia,
                        'gusto_id': record.gusto_id.id,
                        'tipo_doc_id': record.tipo_gusto.id,
                        'name': f"{record.gusto_id.name} - {fecha}"
                    })
                    _logger.info(f"Creando documento para taller '{record.id}' y fecha '{fecha}' y gusto_id '{record.gusto_id.id}'.")
    

    def create_docaem_grupal_records(self):
        """Crear registros en gusto.docaem para talleres grupales."""
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
                    participante.write({'talleres_gusto2_ids': [(4, record.id)]})
                    _logger.info(f"IDs de participante: {participante} , ID_TALLER: {record.id}")
                    for fecha in fechas:
                        # Excluir sábados (5) y domingos (6)
                        if fecha.weekday() in (5, 6):  # 5: Sábado, 6: Domingo
                            _logger.info(f"Excluyendo fecha '{fecha}' porque es fin de semana.")
                            continue
                        
                        
                        # Verificar si ya existe un registro en docaem para este participante, taller y fecha
                        existing_record = self.env['gusto.docaem'].search([
                            ('taller_id', '=', record._origin.id),
                            ('gusto_id', '=', participante._origin.id),
                            ('fecha', '=', fecha),
                        ], limit=1)
                        _logger.info(f"Registros encontrados: {len(existing_record)} para taller_id: {record.id}, gusto_id: {participante.id}, fecha: {fecha}")

                        # Si no existe un registro, crear uno nuevo
                        if not existing_record:
                            self.env['gusto.docaem'].create({
                                'taller_id': record.id,
                                'fecha': fecha,
                                'horas': horas_por_dia,
                                'gusto_id': participante.id,
                                'tipo_doc_id': record.tipo_gusto.id,
                                'name': f"Taller: {record.name} - {participante.participante} - {fecha}",
                                'grupal': True,
                            })
                            _logger.info(f"Documento de taller_id: '{record.id}' gusto_id: '{participante.id}' y fecha: '{fecha}' NO EXISTE y se crea")
                        else:
                            _logger.info(f"Documento de taller_id: '{record.id}' gusto_id: '{participante.id}' y fecha: '{fecha}' EXISTE")
                            
                        """
                        self.env['gusto.docaem'].create({
                            'taller_id': record.id,
                            'fecha': fecha,
                            'horas': horas_por_dia,
                            'gusto_id': participante.id,
                            'tipo_doc_id': record.tipo_gusto.id,
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
            
            _logger.info(f"#####################   Valores recibidos para crear un taller: {vals} . y tambien el gusto id: {self.gusto_id} ")

            # Si vals es un entero, devolver el registro correspondiente (y evitar llamar a create nuevamente)
            #if isinstance(vals, int):
            #    _logger.warning(f"########################   Se recibió un ID en lugar de un diccionario: {vals}. Retornando el registro existente.")
            #    return self.browse(vals)
            
            # Si vals no es un diccionario, lanzar una excepción
            if not isinstance(vals, dict):
                raise ValidationError(f"#######################   Se esperaba un diccionario, pero se recibió: {type(vals).__name__}")
    #
            # Crear el registro con los valores válidos
            res = super(GustoTalleress, self).create(vals)

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

                    # Crear el registro en gusto.docaem
                    self.env['gusto.docaem'].create({
                        'taller_id': res.id,          # ID del taller recién creado
                        # 'tipo_doc_id': res.id_tipo_gusto,
                        'name': f"{res.name} - {fecha}",
                        'fecha': fecha,
                        'horas': res.horas / duracion if duracion > 0 else res.horas,
                    })
            ""
            ##########################################################
            #########################################################
            if 'gusto_id' in vals:
                gusto = self.env['gusto.gusto'].browse(vals['gusto_id'])
                gusto.write({'talleres_gusto_ids': [(4, res.id)]})  # Añadir taller al usuario
                res.write({'participantes_talleres_ids': [(4, gusto.id)]})  # Añadir usuario al taller

            # Crear registros en gusto.docaem
            res.create_docaem_records()

            # Vincular al gusto.gusto si es necesario
            if 'gusto_id' in vals:
                gusto = self.env['gusto.gusto'].browse(vals['gusto_id'])
                _logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$$    El ID del gusto asociado es: {gusto_id}")
                if gusto:
                    _logger.info(f"$$$$$$$$$$$$$$$$$$$$$$   Talleres antes de actualizar en gusto.gusto: {gusto.talleres_gusto_ids.ids}")
                    gusto.write({'talleres_gusto_ids': [(4, res.id)]})
                    _logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$    Talleres después de actualizar en gusto.gusto: {gusto.talleres_gusto_ids.ids}")
    #
                    # Vincular el participante en el taller
                    _logger.info(f"$$$$$$$$$$$$$$$$$   Participantes antes de actualizar en gusto.talleres: {res.participantes_talleres_ids.ids}")
                    res.write({'participantes_talleres_ids': [(4, gusto.id)]})
                    _logger.info(f"$$$$$$$$$$$$$$$$$$$$$$$   Participantes después de actualizar en gusto.talleres: {res.participantes_talleres_ids.ids}")
    #
            return res
    """