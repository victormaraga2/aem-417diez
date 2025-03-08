from odoo import models, fields, api
import base64
import pandas as pd
from io import BytesIO

class CaptacionTalleresImportWizard(models.TransientModel):
    _name = 'captacion.talleres.import.wizard'
    _description = 'Asistente de Importación de Talleres'

    file = fields.Binary(string="Archivo Excel", required=True)
    file_name = fields.Char(string="Nombre del Archivo")

    def action_import_file(self):
        # Verificar que el archivo se haya cargado
        if not self.file:
            raise ValueError("No se ha seleccionado ningún archivo.")
        
        # Leer y decodificar el archivo Excel
        file_content = base64.b64decode(self.file)
        excel_data = pd.read_excel(BytesIO(file_content), engine='openpyxl')

        # Procesar cada fila del archivo Excel
        for index, row in excel_data.iterrows():
            # Obtener o crear registros relacionados
            captacion_id = self.env['res.partner'].browse(row['captacion_id']) if row['captacion_id'] else False
            #provincia_id = self.env['res.country.state'].browse(row['provincia_id']) if row['provincia_id'] else False
            docaem_id = self.env['captacion.docaem'].browse(row['docaem_id']) if row['docaem_id'] else False

            # Obtener participantes de captacion_id para completar los campos Many2many
            participantes_talleres_ids = [(4, part.id) for part in captacion_id]
            participantes_talleres2_ids = [(4, part.id) for part in captacion_id]

            # Crear el registro en captacion.talleres
            self.env['captacion.talleres'].create({
                #'provincia_id': provincia_id.id,
                'fec_inicio': row['fecha_inicio'],
                'fec_fin': row['fecha_fin'],
                'horas': row['horas'],
                'tipo_captacion': row['tipo_captacion'],
                'modalidad': row['modalidad'],
                'name': row['nombre'],
                'captacion_id': captacion_id.id,
                'docaem_ids': [(4, docaem_id.id)] if docaem_id else [],
                'participantes_talleres_ids': participantes_talleres_ids,
                'participantes_talleres2_ids': participantes_talleres2_ids,
            })
