from odoo import models, fields, api, exceptions

class ReservasfServiceEdition(models.Model):
    _name = 'Reservas.service.edition'
    _description = 'Ediciones o Series de Servicios'

    name = fields.Char(string="Nombre de la Edición", required=True)
    service_id = fields.Many2one('product.template', string="Servicio", domain=[('type', '=', 'service')])
    version = fields.Char(string="Versión/Serie", required=True)
    release_date = fields.Date(string="Fecha de Inicio")
    end_date = fields.Date(string="Fecha de Fin")
    price = fields.Float(string="Precio")
    description = fields.Text(string="Descripción")
    active = fields.Boolean(string="Activo", default=True)

    max_participants = fields.Integer(string="Máximo de Participantes", default=10)
    reserve_percentage = fields.Float(string="Porcentaje de Reserva", default=20.0)  # Ejemplo: 20% más de reservas
    participant_ids = fields.One2many('reservas.service.edition.participant', 'edition_id', string="Participantes Confirmados")
    reserve_ids = fields.One2many('reservas.service.edition.reserve', 'edition_id', string="Lista de Reserva")

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('open', 'Abierta'),
        ('in_progress', 'En Curso'),
        ('closed', 'Finalizada'),
    ], string="Estado", default='draft')

    @api.constrains('max_participants', 'reserve_percentage')
    def _check_limits(self):
        if self.max_participants <= 0:
            raise exceptions.ValidationError("El número máximo de participantes debe ser mayor que 0.")
        if self.reserve_percentage < 0:
            raise exceptions.ValidationError("El porcentaje de reserva no puede ser negativo.")

    def action_open_edition(self):
        """Activa la edición y permite que los participantes se registren."""
        self.state = 'open'

    def action_start_edition(self):
        """Cuando inicia la edición, se asignan reservas si hay cupos disponibles."""
        self.state = 'in_progress'
        available_slots = self.max_participants - len(self.participant_ids)

        if available_slots > 0 and self.reserve_ids:
            to_confirm = self.reserve_ids[:available_slots]
            for reserve in to_confirm:
                self.env['reservas.service.edition.participant'].create({
                    'edition_id': self.id,
                    'partner_id': reserve.partner_id.id,
                })
                reserve.unlink()

    def action_close_edition(self):
        """Finaliza la edición y la bloquea para nuevas inscripciones."""
        self.state = 'closed'
