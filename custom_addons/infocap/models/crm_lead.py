from odoo import models, fields, api
from odoo.exceptions import ValidationError
import hashlib
import time
import uuid  # Import the uuid module
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    is_contact_created = fields.Boolean(
        string="¿Es Partipante?",
        compute="_compute_is_contact_created",
        store=True
    )

    documentos_ids = fields.One2many(
        'infocap.documentos',  # Modelo relacionado
        'solicitudes_id',      # Campo Many2one en el modelo relacionado
        string='Documentos Aportados'
    )

    # Campos añadidos para la subida de documentacion
    upload_token = fields.Char(string="Upload Token")
    url = fields.Char(string="URL de subida")

    def generate_upload_token(self):
        self.ensure_one()
        unique_string = str(uuid.uuid4())
        self.upload_token = hashlib.sha256(unique_string.encode()).hexdigest()

    def get_upload_url(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if self.id:
            self.generate_upload_token()
            self.url = f"{base_url}/solicitante/upload/?token={self.upload_token}"  # pass token as parameter
        else:
            self.url = ""

    @api.depends('partner_id')
    def _compute_is_contact_created(self):
        for lead in self:
            lead.is_contact_created = bool(lead.partner_id)

    def action_pasar_a_contacto(self):
        # Verificar si el stage es "Aprobado"
        if self.stage_id.name != "Aprobado":
            raise ValidationError("Esta oportunidad no está en el estado 'Aprobado'.")

        # Buscar si el contacto ya existe en res.partner
        partner = self.env['res.partner'].search([
            ('name', '=', self.contact_name),
            ('email', '=', self.correo),
        ], limit=1)
        if partner:
            raise ValidationError("El partipante ya existe en la base de datos.")
        else:
            # Crear un nuevo contacto en res.partner
            partner = self.env['res.partner'].create({
                'name': self.contact_name, # Nombre del contacto
                'phone': self.telefono, # Teléfono
                'email': self.correo, # Correo electrónico
                'street': self.municipio, # Municipio (puedes ajustar esto según tus campos)
                'comment': self.observacion, # Observaciones
            })

            # Opcional: Asignar el nuevo contacto al crm.lead
            self.partner_id = partner.id

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Éxito',
                'message': 'Los datos se han pasado a Contactos correctamente.',
                'sticky': False,
            }
        }
