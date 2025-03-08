from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    is_contact_created = fields.Boolean(
        string="¿Es Contacto?",
        compute="_compute_is_contact_created",
        store=True
    )

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
            raise ValidationError("El contacto ya existe en la base de datos.")
        else:
            for lead in self:
                # Crear un nuevo contacto en res.partner
                partner = self.env['res.partner'].create({
                'name': lead.contact_name,  # Nombre del contacto
                'phone': lead.telefono,     # Teléfono
                'email': lead.correo,       # Correo electrónico
                'street': lead.municipio,   # Municipio (puedes ajustar esto según tus campos)
                'comment': lead.observacion,  # Observaciones
            })
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

