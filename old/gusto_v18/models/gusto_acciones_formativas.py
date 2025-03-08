
from odoo import models, fields, api, exceptions, _
import re
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)

class GustoAccionesFormativas(models.Model):
    _name = 'gusto.acciones.formativas'
    #_inherit = 'mail.thread'
    _description = 'Registro de acciones formativas sto'



    id_sto = fields.Integer('ID STO')
    name = fields.Char('Nº AF')
    nexp = fields.Char('Nº EXP Vº Bº')
    country_id = fields.Many2one('res.country', string='PAÍS', default=lambda self: self.env.ref('base.es'))
    provincia_ids = fields.Many2many(
        'res.country.state', 
        string='PROVINCIA',
        domain="[('country_id', '=', country_id), ('name', 'in', ['Cádiz', 'Córdoba', 'Granada', 'Huelva', 'Jaén', 'Málaga', 'Sevilla', 'Almería'])]")
    
    ### Campos añadidos por Victor ### 14/01/2025
    ####################################################
    pt_nombre=fields.Char('PT. NOMBRE')                    #   STO -> PT. NOMBRE
    pt_apellido1=fields.Char('PT. APELLIDO1')              #   STO -> PT. APELLIDO1
    pt_apellido2=fields.Char('PT. APELLIDO2')              #   STO -> PT. APELLIDO1

    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    # provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    # company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_id = fields.Many2one(
        'res.company', string="Empresa", default=lambda self: self.env.company, required=True
    )

    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company    
    #####################################################
    
    prev_inicio = fields.Date(string='INICIO PREVISTO')    # Debe heredar de prospestor externo previsto
    prev_fin = fields.Date(string='FIN PREVISTO')          # Debe heredar de prospector externo previsto
    inicio = fields.Date(string='INICIO AF')               # Debe Heredar de STO
    fin = fields.Date(string='FIN AF')                     # Debe Heredar de STO
    accion = fields.Many2one('gusto.accionformativa', string='ACCION')
    # accion = fields.Char('ACCION')
    nombreaccion = fields.Char('DESCRIPCION', related='accion.name')
    modalidad = fields.Selection([('online', 'On line'), ('presencial', 'Presencial')], string='MODALIDAD')
    participantes = fields.Integer(string='Nº PARTICIPANTES')
    prospector_id = fields.Many2one('gusto.prospectores', string='PARTNER')
    formador_id = fields.Many2one('gusto.formadores', string='FORMADOR')
    prospector_factura = fields.Many2one('gusto.formadores', string='FACTURACIÓN')

    recurso = fields.Selection(string='RECURSO', selection=[('interno','INTERNO'),('externo','EXTERNO')])
    estado = fields.Char('ESTADO')
    prosp_form_id = fields.Many2one('gusto.prospectores', string='FORMACION')
    
    contrata_prev = fields.Integer(string='CONTRATACIONES PREV')
    contrata_real = fields.Integer(string='CONTRATACIONES REAL')
    observaciones = fields.Char(string='OBSERVACIONES')
    docente3 = fields.Many2many('gusto.docentes', string='DOCENTES')
    participante_ids = fields.One2many('gusto.gusto', 'acciones_formativas_id', string='PARTICIPANTE')
    participantes_ids = fields.Many2many('gusto.gusto', relation='gusto_aformativa1_rel', string='PARTICIPANTES')

    n_part_prev = fields.Integer('Nº PART. PREV.')
    n_part_real = fields.Integer('Nº PART. REAL')
    presupuesto_solicitado = fields.Float('PRESUPUESTO SOLICITADO')
    coste = fields.Float('COSTE')
    pendiente_justificar = fields.Float('PENDIENTE JUSTIFICAR')
    validacion = fields.Boolean('VALIDACIÓN')
    horas = fields.Float('HORAS ACCION')
   

    gusto_id = fields.Many2one('gusto.gusto')
    #talleres_id = fields.Many2one('gusto.talleres')

    docaem_ids = fields.One2many('gusto.docaem', 'acciones_id', string='DOCUMENTACION')
    unidad = fields.Char('UNIDAD')
    tipo = fields.Char('TIPO')
    pt_nombre=fields.Char('PT. NOMBRE')                    #   STO -> PT. NOMBRE
    pt_apellido1=fields.Char('PT. APELLIDO1')              #   STO -> PT. APELLIDO1
    pt_apellido2=fields.Char('PT. APELLIDO2')              #   STO -> PT. APELLIDO1


    @api.onchange('participantes_ids')
    def _onchange_participantes_ids(self):
        """
        Método onchange que se ejecuta cuando se modifica el campo participantes_ids.
        Abre un wizard para confirmar la creación de registros en docaem.
        """
        
        if self.participantes_ids:
            # self.create_docaem_aformativa_records()
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'gusto.confirm.docaem2.wizard',  # Nombre del wizard
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_acciones_formativas_id': self.id,  # Pasar el ID de la acción formativa al wizard
                },
            }


    @api.model
    def create(self, vals):
        # Llamar al método create original
        record = super(GustoAccionesFormativas, self).create(vals)
        return record

    def write(self, vals):
        # Verificar si se está eliminando un participante
        if 'participantes_ids' in vals:
            # Obtener los participantes actuales antes de la modificación
            current_participantes = self.participantes_ids
            # Obtener los nuevos participantes después de la modificación
            new_participantes = vals.get('participantes_ids', [])
            
            # Si se está eliminando un participante, no crear registros en docaem
            if len(new_participantes) < len(current_participantes):
                # Identificar los participantes eliminados
                deleted_participantes = current_participantes - self.env['gusto.gusto'].browse(new_participantes[0][2])
                # Eliminar los registros en gusto.docaem asociados a los participantes eliminados y a esta acción formativa
                for participante in deleted_participantes:
                    # self.env['gusto.docaem'].search([('gusto_id', '=', participante.id)]).unlink()
                    self.env['gusto.docaem'].search([
                        ('acciones_id', '=', self.id),  # Filtra por la acción formativa actual
                        ('gusto_id', '=', participante.id),  # Filtra por el participante eliminado
                    ]).unlink()

                # return super(GustoAccionesFormativas, self).write(vals)
        
        # Llamar al método write original
        res = super(GustoAccionesFormativas, self).write(vals)
        
        # Verificar si se ha modificado el campo participantes_ids
        if 'participantes_ids' in vals:
        # Verificar si se ha modificado el campo participantes_ids y no se está eliminando un participante
        # if 'participantes_ids' in vals and len(vals.get('participantes_ids', [])) >= len(self.participantes_ids):
            self.create_docaem_aformativa_records()
        
        return res

    """    
    @api.model
    def create(self, vals):
        record = super(GustoAccionesFormativas, self).create(vals)
        if vals.get('modalidad') != 'grupal':
            record.create_docaem_grupal_records()
        return record
    """

    @api.constrains('modalidad', 'provincia_ids')
    def _check_provincia_ids_limit(self):
        for record in self:
            if record.modalidad == 'presencial' and len(record.provincia_ids) > 1:
                raise exceptions.ValidationError("Solo se permite seleccionar una provincia para la modalidad presencial.")


    @api.model
    def default_get(self, fields):
        res = super(GustoAccionesFormativas, self).default_get(fields)
        res['country_id'] = self.env.ref('base.es').id  # Pone por defecto españa
        return res

    def create_docaem_aformativa_records(self):
        """Crear registros en gusto.docaem para acciones formativas grupales."""
        for record in self:
            if record.inicio and record.fin and record.participantes_ids:
                rango_dias = (record.fin - record.inicio).days + 1
                fechas = [record.inicio + timedelta(days=i) for i in range(rango_dias)]

                # Filtrar solo los días laborables (lunes a viernes)
                dias_laborables = [fecha for fecha in fechas if fecha.weekday() not in (5, 6)]  # Excluir sábados y domingos

                # Calcular las horas por día según los días laborables
                rango_dias_laborables = len(dias_laborables)
                horas_por_dia = record.horas / rango_dias_laborables if rango_dias_laborables > 0 else 0

                for participante in record.participantes_ids:
                    for fecha in fechas:
                        # Excluir sábados (5) y domingos (6)
                        if fecha.weekday() in (5, 6):  # 5: Sábado, 6: Domingo
                            _logger.info(f"Excluyendo fecha '{fecha}' porque es fin de semana.")
                            continue

                        # Verificar si ya existe un registro en docaem para este participante y fecha
                        existing_record = self.env['gusto.docaem'].search([
                            ('acciones_id', '=', record._origin.id),
                            ('gusto_id', '=', participante._origin.id),
                            ('fecha', '=', fecha),
                        ], limit=1)
                        _logger.info(f"Registros encontrados para Acción Formativa: {len(existing_record)} para taller_id: {record.id}, gusto_id: {participante.id}, fecha: {fecha}")
                        
                        # Si no existe un registro, crear uno nuevo
                        if not existing_record:
                            self.env['gusto.docaem'].create({
                                'acciones_id': record.id,
                                'fecha': fecha,
                                'horas': horas_por_dia,
                                'gusto_id': participante.id,
                                'name': f"Acción Formativa: {record.name} - {participante.participante} - {fecha}",
                                'grupal': False,
                            })
                            _logger.info(f"Documento de Acción Formativa taller_id: '{record.id}' gusto_id: '{participante.id}' y fecha: '{fecha}' NO EXISTE y se crea")
                        else:
                            _logger.info(f"Documento de Acción Formativa taller_id: '{record.id}' gusto_id: '{participante.id}' y fecha: '{fecha}' EXISTE")
                        

