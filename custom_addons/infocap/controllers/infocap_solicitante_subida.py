from odoo import http
from odoo.http import request
import hashlib
import time
import base64
import uuid
import logging

_logger = logging.getLogger(__name__)

class SolicitanteSubidaController(http.Controller):

    @http.route('/solicitante/upload/', type='http', auth='public', website=True, methods=['GET'])
    def upload_document(self, **kwargs):
        # Get the token from the request parameters
        token = request.params.get('token')
        if not token:
            return "No token provided"

        # Buscar el lead asociado al token
        lead = request.env['crm.lead'].sudo().search([('upload_token', '=', token)], limit=1)

        # Si no existe, renderizar una página 404
        if not lead:
            return request.render('infocap.404_template', {})

        # Pasar el lead al template
        return request.render('infocap.infocap_solicitante_upload_form', {'lead': lead})

    @http.route('/solicitante/upload/submit', type='http', auth='public', website=True, methods=['POST'])
    def upload_submit(self, **post):
        token = request.params.get('token')  # Get token from request.params
        lead = request.env['crm.lead'].sudo().search([('upload_token', '=', token)], limit=1)
        if not lead:
            return request.redirect('/')

        files = {
            'dni1': post.get('dni1'),
            'dni2': post.get('dni2'),
            'vida_laboral': post.get('vida_laboral'),
            'demanda': post.get('demanda')
        }
        
        for field_name, file in files.items():
            if field_name == 'dni1':
                file_type = 2
            elif field_name == 'dni2':
                file_type = 2
            elif field_name == 'vida_laboral':
                file_type = 3
            elif field_name == 'demanda':
                file_type = 4
            if file and hasattr(file, 'filename'):
                try:
                    #attachment = request.env['ir.attachment'].sudo().create({
                    #    'name': file.filename,
                    #    'datas': base64.b64encode(file.read()),  # Use base64 encoding
                    #    'res_model': 'crm.lead',
                    #    'res_id': lead.id,
                    #    'type': 'binary',
                    #    'description': f"Archivo subido para {field_name}"  # Optional description
                    #})
                    file_content = file.read()
                    file_base64 = base64.b64encode(file_content)
                    attachment = request.env['infocap.documentos'].sudo().create({
                        'name': file.filename,
                        'document_file': file_base64,  # Use base64 encoding
                        'document_type_id': file_type, # Cambiar por el tipo de file file.[0]
                        'solicitudes_id': lead.id,
                        'fecha': time.strftime('%Y-%m-%d'),
                        
                    })
                    _logger.info(f"Archivo {file.filename} subido y adjuntado al lead {lead.id}")  # Log the successful upload
                except Exception as e:
                    _logger.error(f"Error creating attachment for {field_name}: {e}")
                    return f"Error uploading {field_name}: {e}"  # Specific error message
        return request.redirect('/contactus-thank-you')