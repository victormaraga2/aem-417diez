from odoo import models, fields, api
import base64
import csv
from io import StringIO

class GustoImportcsvEtiquetasWizard(models.TransientModel):
    _name = 'gusto.importcsv.etiquetas.wizard'
    _description = 'Import CSV for modelo_A'

    csv_file = fields.Binary(string='CSV File', required=True)
    csv_filename = fields.Char(string='File Name')
    csv_record_count = fields.Integer(string='CSV Records', readonly=True)

    


    update_needed_count = fields.Integer(string='Records Requiring Update', readonly=True)
    no_counter = fields.Integer(string='No Pasa', readonly=True)
    datocsv = fields.Char('datocsv')
    datobase = fields.Char('datobase')
    def process_csv(self):
        # Decodificar el archivo CSV
        csv_data = base64.b64decode(self.csv_file)
        data_file = StringIO(csv_data.decode("utf-8"))
        data_file.seek(0)
        file_reader = []
        reader = csv.reader(data_file, delimiter=',')
        
        csv_record_counter = 0
        update_needed_counter = 0
        no_counter = 0

        

        # Leer cada fila del archivo CSV y contar registros
        for row in reader:
            csv_record_counter += 1
            name = row[0]
            descripcion = row[1] 
            comentario = row[2] 
            
            
            # Buscar si el registro ya existe en modelo_A
            #record = self.env['gusto.gusto'].search([('name', '=', name.upper())], limit=1)
            record = self.env['gusto.tipo_contratoss'].search([('name', '=', name)], limit=1)
            
            if record:
                # Verificar si necesita actualización
                #if (record.telefono != telefono or
                #    record.correo != correo):
                update_needed_counter += 1
            else:
                no_counter += 1
            

        # Actualizar los contadores en el formulario
        self.csv_record_count = csv_record_counter
        self.update_needed_count = update_needed_counter
        self.no_counter = no_counter
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'gusto.importcsv.telefono.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def update_records(self):
        # Decodificar el archivo CSV
        csv_data = base64.b64decode(self.csv_file)
        data_file = StringIO(csv_data.decode("utf-8"))
        data_file.seek(0)
        file_reader = []
        reader = csv.reader(data_file, delimiter=',')
        
       
        # Actualizar cada fila del archivo CSV
        for row in reader:
            name = row[0]
            
            
            # Buscar si el registro ya existe en modelo_A
            record = self.env['res.partner'].search([('name', '=', name.upper())], limit=1)
            #record = self.env['gusto.tipo.contratoss'].search([('name', '=', name)], limit=1)
            if record:
                self.env['gusto.taghorarios'].create({
                    'name': 'JORNADA COMPLETA',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env['gusto.taghorarios'].create({
                    'name': 'MEDIA JORNADA',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env['gusto.taghorarios'].create({
                    'name': 'TURNOS ROTATIVOS',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env['gusto.taghorarios'].create({
                    'name': 'TURNO DE NOCHE',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env['gusto.taghorarios'].create({
                    'name': 'FLEXIBILIDAD HORARIA',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                
                

                self.env['gusto.tagprl'].create({
                    'name': '60H',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env['gusto.tagprl'].create({
                    'name': 'ESTRUCTURAS METALICAS',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env['gusto.tagprl'].create({
                    'name': 'ELECTRICIDAD',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })

                

                self.env['gusto.tagcolectivos'].create({
                    'name': 'MENOR 30',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env['gusto.tagcolectivos'].create({
                    'name': 'GARANTIA JUVENIL',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env['gusto.tagcolectivos'].create({
                    'name': 'MAYOR 52',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env['gusto.tagcolectivos'].create({
                    'name': 'DISCAPACIDAD',
                    'sino': False,  # Representa 1 como True
                    'gusto_id': record.id
                })
                self.env.cr.commit()
           

            
            
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'gusto.importcsv.telefono.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def cancel_update(self):
        # Acción para cancelar y salir del formulario
        return {'type': 'ir.actions.act_window_close'}