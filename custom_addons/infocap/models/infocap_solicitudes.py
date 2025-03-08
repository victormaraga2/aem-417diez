
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import hashlib
import time


class InfocapSolicitudes(models.Model):
    _description = 'Registro de solicitudes'
    _inherit = 'crm.lead'

    es_participante = fields.Boolean(
        string="¿Es Partipante?",
        compute="_compute_es_participante",
        store=True
    )
    
    

    # city = fields.Many2one(city)
    municipio = fields.Char(string ='Municipio')
    country_id = fields.Many2one('res.country', string='PAÍS', default=lambda self: self.env.ref('base.es'))
    state_id = fields.Many2one('res.country.state', string='Provincia', domain="[('country_id', '=', country_id)]")
    dni = fields.Char(string='DNI')

    programa_id = fields.Many2one('infocap.programas', string='Programa')
    proyecto_id = fields.Many2one('infocap.proyectos', string='Proyecto', domain="[('programa_id', '=', programa_id)]")
    convocatoria_id = fields.Many2one('infocap.convocatoria', string='Convocatoria', domain="[('programa_id', '=', programa_id)]")
    nombre = fields.Char(string='Nombre')  # Cambio para recopilar LandingPage y poder realizar posterior informes
    apellidos = fields.Char(string='Apellidos') # Cambio para recopilar LandingPage y poder realizar posterior informes
    name = fields.Char(default='solicitud', stored='True')

    ref_url = fields.Char(string='URL de Referencia')
    genero = fields.Selection(string="Genero",
                             selection=[('femenino', 'Femenino'),
                                        ('masculino', 'Masculino')])
    fecha_carga = fields.Date(string='Fecha Carga')
    fecha_nacimiento = fields.Date(string='Fecha Nacimiento')
    situacion = fields.Many2one('infocap.situacion', string='Situación')
    garantia = fields.Boolean(string='Garantía Juvenil')
    sae = fields.Boolean(string='Demandante Empleo')
    objetivo_profesional = fields.Many2one('infocap.objetivoprofesional',string='Objetivo Profesional')
    preferencia = fields.Many2one('infocap.interesesprofesionales', string='Preferencia')
    procedencia = fields.Char(string='Procedencia')

    #programa_id = fields.Many2one('infocap.programas', string='Programa', domain="[('proyecto_id', '=', proyecto_id)]" )
    #convocatoria_id = fields.Many2one('infocap.convocatoria', string='Convocatoria', domain="[('programa_id', '=', programa_id)]")
    #name = fields.Char(default='solicitud')

    producto_id = fields.Many2one(
        'product.product',
        string='Solicita participar',
        domain="[('convocatoria_ids', 'in', convocatoria_id)]"
    )

    producto2_id = fields.Many2many(
        'product.product',
        string='Solicita prueba',
        domain="[('convocatoria_ids', 'in', convocatoria_id)]"
    )

    colectivo_id = fields.Many2one('infocap.colectivo', string='Colectivo')
    
    anos_exp = fields.Integer(string='Años Experiencia')

    #documentos_ids = fields.Many2many(
    #    string='Documentos',
    #    comodel_name='ir.attachment'
    #)
    documentos_ids = fields.One2many(
        'infocap.documentos',
        'solicitudes_id',
        string='Documentos'
    )

    # Calculuar automáticamente la letra del DNI
    @api.onchange('dni')
    def _onchange_dni(self):
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
        for record in self:
            if record.dni and record.dni[:-1].isdigit() and len(record.dni) == 9:
                numero = int(record.dni[:-1])
                letra_correcta = tabla[numero % 23]
                # Reemplazar la última letra si es incorrecta
                record.dni = f"{numero}{letra_correcta}"


    @api.depends('partner_id')
    def _compute_es_participante(self):
        for lead in self:
            partner = self.env['res.partner'].search([('id', '=', lead.partner_id.id)], limit=1)
            
            if partner:
                lead.is_contact_created = partner.es_participante
            else:
                lead.is_contact_created = False  # Si el contacto no existe, reflejarlo en lead



    def action_pasar_a_contacto(self):
        # Verificar si el stage es "Aprobado"
        if self.stage_id.name != "Aprobado":
            raise ValidationError("Esta oportunidad no está en el estado 'Aprobado'.")

        # Buscar si el contacto ya existe en res.partner
        partner = self.env['res.partner'].search([
            ('name', '=', self.contact_name),
            ('email', '=', self.email_from),
        ], limit=1)

        if partner:
            raise ValidationError("El partipante ya existe en la base de datos.")
        else:
            for lead in self:
                # Crear un nuevo contacto en res.partner
                partner = self.env['res.partner'].create({
                'name': lead.contact_name,  # Nombre del contacto
                'phone': lead.phone,     # Teléfono
                'email': lead.email_from,       # Correo electrónico
                'country_id': lead.country_id.id,
                'city': lead.municipio,   # Municipio 
                'state_id': lead.state_id.id,   # Provincia
                'comment': lead.description,  # Observaciones
                'es_participante': True,
                'documentos_ids': [(6, 0, [doc.id for doc in lead.documentos_ids])],               

            })
            # vaciar el token
            lead.upload_token = ''
            lead.url = ''
            
            # Opcional: Asignar el nuevo contacto al crm.lead
            lead.partner_id = partner.id
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Éxito',
                    'message': 'Los datos se han pasado a Contactos correctamente.',
                    'sticky': False,
                }
            }
    
    @api.depends('nombre', 'apellidos')
    def _compute_nombrecompleto(self):
        for rec in self:
            rec.name = rec.nombre + ' ' + rec.apellidos