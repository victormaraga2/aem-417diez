
from odoo import models, fields, api


class InfocapConvocatoria(models.Model):
    _name = 'infocap.convocatoria'
    _description = 'Registro de comvocatoria'


    name = fields.Char('Convocatoria', required=True)
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincias_ids = fields.Many2many('res.country.state', string="Provincias", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='EMPRESAS',required=False,)#default=lambda self: self.env.company)
    #denominacion = fields.Char('Convocatoria')
    situacion = fields.Selection([('abierto','ABIERTO'), ('cerrado','CERRADO'),], string="Estado")
    observaciones = fields.Char('Observaciones')

    
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
    max_participantes = fields.Integer('Máximo de participantes', required=True)
    ediciones_ids = fields.One2many('infocap.ediciones', 'convocatoria_id', string='Ediciones de Cursos')
    total_participantes = fields.Integer(string='Participantes', compute='_compute_total_participantes', store=True)
    

   
    #programa_id = fields.Many2one('infocap.programas', string='Programa')
    #proyecto_id = fields.Many2one('infocap.proyectos', string='Proyecto')
    programa_id = fields.Many2one('infocap.programas', string='Programa', required=True)
    proyecto_id = fields.Many2one('infocap.proyectos', string='Proyecto', required=True, domain="[('programa_id', '=', programa_id)]")
    

    productos_ids = fields.Many2many('product.product', string='Solicitud')

    producto_id = fields.Many2one(
        'product.product', 
        string='Producto'
    )

    ## Configura los productos de la convocatoria. Se pone como One2many porsi 
    ## hay ampliaciones de la convocatoria
    productos_convocatorias_ids = fields.One2many(
        'infocap.productos_convocatorias',
        'convocatoria_id',
        string='Productos de Convocatorias'
    )   

    @api.depends('ediciones_ids.participantes_ids')
    def _compute_total_participantes(self):
        """Suma los participantes de todas las versiones de curso dentro de la convocatoria"""
        for record in self:
            record.total_participantes = sum(len(version.participantes_ids) for version in record.ediciones_ids)

    @api.constrains('total_participantes', 'max_participantes')
    def _check_limite_participantes(self):
        """Evita que el número total de participantes supere el límite de la convocatoria"""
        for record in self:
            if record.total_participantes > record.max_participantes:
                raise models.ValidationError('El número total de participantes supera el límite de la convocatoria.')



    
    




    