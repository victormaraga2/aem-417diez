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
            # self.create_docaem_grupal_records()            
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
        modalidad = self.env.context.get('default_modalidad', vals.get('modalidad'))
        captacion_id = self.env.context.get('default_captacion_id')

        if modalidad == 'individual':
            if not captacion_id:
                raise ValidationError("El 'captacion_id' es obligatorio para la modalidad individual.")
            taller = super(CaptacionTalleress, self).create(vals)
            taller.write({'participantes_talleres_ids': [(4, int(captacion_id))]})
            taller.create_docaem_individual_records()
            return taller

        elif modalidad == 'grupal':
            taller = super(CaptacionTalleress, self).create(vals)
            command = vals.get('participantes_talleres_ids', [])
            if command and isinstance(command[0], (list, tuple)) and len(command[0]) >= 3:
                participantes_ids = command[0][2]
                for participante in participantes_ids:
                    taller.write({'participantes_talleres_ids': [(4, participante)]})
                taller.create_docaem_grupal_records()
            return taller

    def write(self, vals):
        # Evitar la creación de registros en docaem al eliminar participantes
        if 'participantes_talleres_ids' in vals:
            for record in self:
                # Eliminar documentos asociados a los participantes eliminados
                if record.modalidad == 'grupal':
                    old_participantes = record.participantes_talleres_ids
                    new_participantes = self.env['res.partner'].browse(vals['participantes_talleres_ids'][0][2])
                    removed_participantes = old_participantes - new_participantes

                    # Eliminar documentos asociados a los participantes eliminados
                    for participante in removed_participantes:
                        self.env['captacion.docaem'].search([
                            ('taller_id', '=', record.id),
                            ('captacion_id', '=', participante.id)
                        ]).unlink()

        res = super(CaptacionTalleress, self).write(vals)

        # Crear registros en docaem solo si no se están eliminando participantes
        if 'participantes_talleres_ids' in vals and not self.env.context.get('skip_docaem_creation', False):
            for record in self:
                if record.modalidad == 'grupal':
                    record.create_docaem_grupal_records()

        return res

    def create_docaem_individual_records(self):
        """Crear registros en captacion.docaem según la duración del taller."""
        for record in self:
            if record.fec_inicio and record.fec_fin and record.captacion_id:
                rango_dias = (record.fec_fin - record.fec_inicio).days + 1
                fechas = [record.fec_inicio + timedelta(days=i) for i in range(rango_dias)]
                dias_laborables = [fecha for fecha in fechas if fecha.weekday() not in (5, 6)]
                horas_por_dia = record.horas / len(dias_laborables) if dias_laborables else 0

                for fecha in fechas:
                    if fecha.weekday() in (5, 6):
                        continue
                    self.env['captacion.docaem'].create({
                        'taller_id': record.id,
                        'fecha': fecha,
                        'horas': horas_por_dia,
                        'captacion_id': record.captacion_id.id,
                        'tipo_doc_id': record.tipo_captacion.id,
                        'name': f"{record.captacion_id.name} - {fecha}"
                    })

    def create_docaem_grupal_records(self):
        """Crear registros en captacion.docaem para talleres grupales."""
        for record in self:
            if record.fec_inicio and record.fec_fin and record.participantes_talleres_ids:
                rango_dias = (record.fec_fin - record.fec_inicio).days + 1
                fechas = [record.fec_inicio + timedelta(days=i) for i in range(rango_dias)]
                dias_laborables = [fecha for fecha in fechas if fecha.weekday() not in (5, 6)]
                horas_por_dia = record.horas / len(dias_laborables) if dias_laborables else 0

                for participante in record.participantes_talleres_ids:
                    for fecha in fechas:
                        if fecha.weekday() in (5, 6):
                            continue
                        existing_record = self.env['captacion.docaem'].search([
                            ('taller_id', '=', record.id),
                            ('captacion_id', '=', participante.id),
                            ('fecha', '=', fecha),
                        ], limit=1)
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

    def unlink(self):
        """Eliminar documentos asociados al taller cuando se elimina el taller."""
        for record in self:
            self.env['captacion.docaem'].search([('taller_id', '=', record.id)]).unlink()
        return super(CaptacionTalleress, self).unlink()   