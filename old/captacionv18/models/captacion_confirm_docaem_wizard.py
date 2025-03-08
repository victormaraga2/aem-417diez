from odoo import models, fields, api

class CaptacionConfirmDocaemWizard(models.TransientModel):
    _name = 'captacion.confirm.docaem.wizard'
    _description = 'Confirmación de creación de registros en captacion.docaem'

    talleres_id = fields.Many2one('captacion.talleres', string="Taller")

    def confirm_creation(self):
        """Acción al confirmar la creación de registros."""
        if self.talleres_id:
            self.talleres_id.create_docaem_records()
