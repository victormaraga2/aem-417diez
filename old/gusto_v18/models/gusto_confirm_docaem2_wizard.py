from odoo import models, fields, api

class ConfirmDocaem2Wizard(models.TransientModel):
    _name = 'gusto.confirm.docaem2.wizard'
    _description = 'Wizard para confirmar la creación de registros en docaem'

    acciones_formativas_id = fields.Many2one('gusto.acciones.formativas', string='Acción Formativa', required=True)

    def confirm_create_docaem(self):
        """
        Método para confirmar la creación de registros en docaem.
        """
        self.acciones_formativas_id.create_docaem_aformativa_records()
        return {'type': 'ir.actions.act_window_close'}  # Cerrar el wizard después de confirmar