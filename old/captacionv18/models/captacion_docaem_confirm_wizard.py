
from odoo import models, fields, api, _

class CaptacionDocaemConfirmWizard(models.TransientModel):
    _name = 'captacion.docaem.confirm.wizard'
    _description = 'Confirmar Actualización de Documentos'

    docaem_vals = fields.Text(string="Valores a Crear", required=True)
    taller_id = fields.Many2one('captacion.talleres', string="Taller", required=True)

    def action_confirm_update(self):
        """Crear registros en captacion.docaem basados en los valores confirmados."""
        docaem_vals = eval(self.docaem_vals)  # Convertir texto a lista de diccionarios
        if docaem_vals:
            self.env['captacion.docaem'].create(docaem_vals)

    def action_cancel_update(self):
        """Cancelar la actualización y no realizar cambios."""
        return
