
from odoo import models, fields, api


class GustoOportunidad(models.Model):
    #_name = 'crm_gusto.participantes'
    _description = 'Registro de participantes'
    _inherit = 'crm.lead'



    proyecto_id = fields.Many2one('gusto.proyectos', string='Proyecto')
    #proyecto = fields.Selection(selection=[], compute="_compute_proyecto", string="Proyecto", store=True)
    programa_id = fields.Many2one('gusto.programas', string='Programa', domain="[('proyecto_id', '=', proyecto_id)]" )
    #programa = fields.Selection(selection=[], compute="_compute_programa", string="Programa", store=True)
    convocatoria_id = fields.Many2one('gusto.convocatoria', string='Convocatoria', domain="[('programa_id', '=', programa_id)]")

    # producto_id = fields.Many2one('product.product', string= 'Solicita participar', domain="[('convocatia_id', '=', convocatoria_id)]")
    producto_id = fields.Many2one(
    'product.product',
    string='Solicita participar',
    domain="[('convocatoria_ids', 'in', convocatoria_id)]")
    
    #producto_id_name = fields.Char( related = 'producto_id.name', string= 'Producto')
    name = fields.Char(compute='_compute_asunto')


    ## Campos añadidos de participantes (gusto_gusto.py)
    name=fields.Char('DNI/NIE', index=True)                            #   STO -> NIF/NIE
    provincia=fields.Char(string='PROVINCIA', index=True)                     #   STO -> PROVINCIA
    participante=fields.Char('PARTICIPANTE', index=True)               #   STO -> PARTICIPANTE
    pt_nombre=fields.Char('PT. NOMBRE')                    #   STO -> PT. NOMBRE
    pt_apellido1=fields.Char('PT. APELLIDO1')              #   STO -> PT. APELLIDO1
    pt_apellido2=fields.Char('PT. APELLIDO2')              #   STO -> PT. APELLIDO1
    unidad=fields.Char('UNIDAD')                           #   STO -> UNIDAD
    alta_sto=fields.Date('F. ALTA STO')                    #   STO -> FECHA INICIO
    baja_sto=fields.Date('F. BAJA STO')                    #   STO -> FECHA FIN
    colectivo=fields.Many2one('gusto.colectivo', index=True)           #   STO -> COLECTIVO
    inicio_atencion=fields.Date('INICIO ATENCIÓN')         #   STO -> FECHA INICIO ATENCION
    fin_atencion=fields.Date('FIN ATENCIÓN')               #   STO -> FECHA FIN ATENCION
    h_orienta=fields.Char('H. ORIENTACIÓN')                #   STO -> H. HORIENTA
    h_forma=fields.Char('H. FORMACIÓN')                    #   STO -> H. FORMACION
    recibi=fields.Date('INCENTIVO')                        #   STO -> FECHA RECIBI
    inicio_inserccion=fields.Date('INICIO INSERCCIÓN')     #   STO -> FECHA INICIO INSERCCION
    fin_inserccion=fields.Date('FIN INSERCCIÓN')           #   STO -> FECHA FIN INSERCCION
    h_fase_inserccion=fields.Char('H. FASE INSERCCIÓN')    #   STO -> H. FASE INSERCCION -> ACTUAL OI4OH
    d_fase_inserccion=fields.Char('D. FASE INSERCCIÓN')    #   STO -> D. FASE INSERCCION -> NUEVO
    id_participante_sto = fields.Integer('ID_STO', index=True)         #   PREVISTO STO
    dias_fase_insercion = fields.Integer('DIAS F. INSERCION')  #   STO -> DIAS FASE INSERCCIO

    ### Campos añadidos por Victor ### 14/01/2025
    #######################################################
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company
    #######################################################


    ######################################################################################################
    #
    # CAMPOS AUXILIARES
    #
    ######################################################################################################
    # PENDIENTE -> CONECTAR CON PROYECTO 
    # PENDIENTE -> INCLUIR ID PROYECTO
    # PENDIENTE -> PREVEER CONECION CON UNIDAD -> ute
    # PENDIENTE -> INCLUIR ID UTE
    # 

    municipio=fields.Char('MUNICIPIO')                     ##########       GUSTO
    foto_participante=fields.Binary("FOTO")                ##########       GUSTO
    telefono=fields.Char("TELÉFONO")                       ##########       GUSTO
    correo=fields.Char("CORREO")                           ##########       GUSTO
    anos_exp=fields.Char('AÑOS EXP')                       ##########       GUSTO
    observacion = fields.Char("OBSERVACIÓN")               ##########       GUSTO
    #larma = fields.Boolean(string="AV.", default=False)   ##########       GUSTO

    ### Campos añadidos por Victor ### 14/01/2025
    #######################################################
    country_id = fields.Many2one('res.country', string="País", default=lambda self: self.env.ref('base.es'))  # Por defecto, España
    provincia_id = fields.Many2one('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    provincia_ids = fields.Many2many('res.country.state', string="Provincia", domain="[('country_id', '=', country_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=False,)#default=lambda self.env.company,)
    company_ids = fields.Many2many('res.company',string='Empresas Compartidas',required=False,)#default=lambda self: self.env.company
    #######################################################


    ######################################################################################################
    #
    # CAMPOS AUXILIARES
    #
    ######################################################################################################
    # PENDIENTE -> CONECTAR CON PROYECTO 
    # PENDIENTE -> INCLUIR ID PROYECTO
    # PENDIENTE -> PREVEER CONECION CON UNIDAD -> ute
    # PENDIENTE -> INCLUIR ID UTE
    # 

    municipio=fields.Char('MUNICIPIO')                     ##########       GUSTO
    foto_participante=fields.Binary("FOTO")                ##########       GUSTO
    telefono=fields.Char("TELÉFONO")                       ##########       GUSTO
    correo=fields.Char("CORREO")                           ##########       GUSTO
    anos_exp=fields.Char('AÑOS EXP')                       ##########       GUSTO
    observacion = fields.Char("OBSERVACIÓN")               ##########       GUSTO
    #larma = fields.Boolean(string="AV.", default=False)   ##########       GUSTO


    @api.onchange('producto_id') 
    def _compute_asunto(self):
        for rec in self:
            rec.name = rec.producto_id.name
    #        a = 0
 

    #@api.depends('proyecto_id')
    #def _compute_proyecto(self):
    #    for record in self:
    #        if record.proyecto_id:
    #            record.proyecto = record.proyecto_id.name
    #        else:
    #            record.tipo_proyecto = False
    
    #@api.depends('programa_id')
    #def _compute_programa(self):
    #    for record in self:
    #        if record.programa_id:
    #            if record.programa_id.proyecto_id == record.proyecto_id.id:
    #                record.programa = record.programa_id.name
    #        else:
    #            record.programa = False




    