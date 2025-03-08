from odoo import models, fields, api, _


class CaptacionDocaem(models.Model):
    _name = 'captacion.docaem'
    _description = 'Documentos Andalucia Emplea Mas'

    id = fields.Integer(string='ID')
    tipo_doc_id = fields.Many2one('captacion.tipo.doc', string='Tipo Documento')#, required=True)
    grupal = fields.Boolean(string='Grupal', default=False) 
    name = fields.Char(string='Nombre')
    fecha = fields.Date(string='Fecha')
    horas = fields.Integer(string='HORAS')

    ### Campos añadidos por Victor ### 14/01/2025
    ####################################################
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company)
    ####################################################
    
    # Campo para archivo con límite de 5MB
    archivo = fields.Binary(string='Archivo')
    archivo_nombre = fields.Char(string='Nombre del Archivo')  # Campo auxiliar para el nombre del archivo

    captacion_id = fields.Many2one('res.partner')
    participante_captacion = fields.Char(related='captacion_id.participante', string='PARTICIPANTE')
    captacion_id_id = fields.Integer(related='captacion_id.id', string='ID CAPTACION', store=True)

   # captacion_ids = fields.One2many('res.partner', 'taller_id')

    taller_id = fields.Many2one('captacion.talleres')
    taller_id_sto = fields.Integer(related='taller_id.id_sto', string='ID_STO T.')
    taller_id_id = fields.Integer(related='taller_id.id', string='ID_TALLER')

    acciones_id = fields.Many2one('captacion.acciones.formativas')

    contrato_id = fields.Many2one('captacion.contratos', string='CONTRATO')

    # Visor de documento
    def action_open_file_viewer(self):
        # Devuelve la vista del archivo en un formulario popup
        return {
            'name': 'Visor de Archivo',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'captacion.docaem',
            'res_id': self.id,  # Abre el archivo del registro actual
            'views': [(self.env.ref('captacion.view_file_viewer_form').id, 'form')],
            'target': 'new',  # Abrir en un popup
        }
    

    ###############################  Añadido por Víctor 21/01/2025   ##########################
    ###########################################################################################
    #def create_docaem_records(self):
    #    """Crear registros en captacion.docaem según la duración del taller."""
    #    for record in self:
    #        if record.fec_inicio and record.fec_fin and record.captacion_id:
    #            rango_dias = (record.fec_fin - record.fec_inicio).days + 1
    #            fechas = [record.fec_inicio + timedelta(days=i) for i in range(rango_dias)]
    #            for fecha in fechas:
    #                self.env['captacion.docaem'].create({
    #                    'taller_id': record.id,
    #                    'fecha': fecha,
    #                    'horas': record.horas / rango_dias if rango_dias > 0 else 0,
    #                    'participante': record.captacion_id.id,
    #                    'tipo_doc_id': record.tipo_captacion.id,
    #                    'name': f"{record.captacion_id.name} - {fecha}"
    #                })
    ##########################################################################################
