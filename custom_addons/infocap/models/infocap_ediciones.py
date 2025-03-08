from odoo import models, fields, api, _
from datetime import datetime, date, timedelta


class InfocapEdiciones(models.Model):

    _name = 'infocap.ediciones'
    _description = 'Versiones de Cursos'

    name = fields.Char(string='Nombre de la versión', required=True)
    curso_id = fields.Many2one('product.template', string='Curso', required=True)
    docente_id = fields.Many2one('res.partner', string='Docente', domain=[('es_docente', '=', True)])
    fecha_inicio = fields.Date(string='Fecha de Inicio', required=True)
    fecha_final = fields.Date(string='Fecha de Finalización', required=True)
    comunicado = fields.Selection(string="Comunicado", default="opcion1",
                             selection=[('opcion1', 'Opción 1'),
                                        ('opcion2', 'Opción 2'),
                                        ('opcion3', 'Opción 3')])
    
                                        
    fecha_comunicado = fields.Date(string='Fecha de Comunicado')
    contador_participantes = fields.Integer(string='Participantes', compute='_compute_contador_participantes', store=True)

    convocatoria_id = fields.Many2one('infocap.convocatoria', string='Convocatoria')  # Referencia al modelo correcto
    participantes_ids = fields.Many2many('res.partner', string='Participantes',
                                         domain=[('es_participante', '=', True)])
    max_participantes = fields.Integer(string='Máximo de Participantes', default=15)

    @api.constrains('participantes_ids', 'max_participantes')
    def _check_max_participantes(self):
        for record in self:
            if len(record.participantes_ids) > record.max_participantes:
                raise models.ValidationError('El número de participantes supera el límite permitido.')
    
    @api.depends('participantes_ids')
    def _compute_contador_participantes(self):
        for record in self:
            if len(record.participantes_ids):
                record.contador_participantes = len(record.participantes_ids)
            else:
                record.contador_participantes = 0   

    @api.constrains('participantes_ids', 'max_participantes', 'convocatoria_id')
    def _check_limites_participantes(self):
        """Verifica que no se supere el límite de participantes en la versión de curso ni en la convocatoria"""
        for record in self:
            if len(record.participantes_ids) > record.max_participantes:
                raise models.ValidationError('El número de participantes de esta versión de curso supera el límite permitido.')

            # Validar que la suma de participantes en la convocatoria no supere su límite
            if record.convocatoria_id and record.convocatoria_id.total_participantes > record.convocatoria_id.limite_participantes:
                raise models.ValidationError('El total de participantes en la convocatoria supera el límite permitido.')

    
    
   