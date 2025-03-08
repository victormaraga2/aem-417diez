# -*- coding: utf-8 -*-
{
    'name': "inforef",

    'summary': """
        Gestión para la integración laboral, la formación y el empleo""",

    'description': """
        Gestión para la integración laboral, la formación y el empleo
    """,

    'author': "Centro Tecnoformación",
    'website': "https://tecno-formacion.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'crm', 'sale'],

    'assets': {
    'web.assets_backend': [
         #'gusto/static/src/css/captacion.css',   
    ],
    },
    'installable': True,
    'application': True,

    # always loaded
    'data': [
        'security/inforef_gestion_grupos.xml',
        'security/ir.model.access.csv',
        #'security/ir.model.access.orientacion.csv',

        
        #'views/inforef_acciones_formativas.xml',
        #'views/gustos_talleres.xml',
        #'views/gustos_contratos.xml',
        #'views/gustos_contratos_sum.xml',
        #'views/gustos_prospectores.xml',
        #'views/gustos_formadores.xml',

        'views/inforef_interesesprofesionales.xml',
        'views/inforef_productos.xml',
        'views/inforef_necesidadesformacionespecifica.xml',
        'views/inforef_objetivoprofesional.xml',
        'views/inforef_participantes.xml',
        'views/inforef_proyectos.xml',
        'views/inforef_programas.xml',
        'views/inforef_convocatorias.xml',
        'views/inforef_solicitudes.xml',

        # PARAMETRICAS
        'views/inforef_docentes.xml',
        'views/inforef_colectivo.xml',
        'views/inforef_sectorocupacion.xml',
        'views/inforef_perfilocupacion.xml',
        'views/inforef_tipo_jornada.xml',
        'views/inforef_tipo_documento.xml',
        'views/inforef_tipo_taller.xml',
        'views/inforef_tipo_accionformativa.xml',
        'views/inforef_fileviewer.xml',
        

        # NECESARIAS
        
       
        
        ##'views/gustos_docentes_acciones.xml',
        ##'views/gustos_perfiles_participantes.xml',
        ##'views/gustos_tipo_documento.xml',
        #'views/gustos_tag.xml',
        #'views/gustos_tipo_tag.xml',
        #'views/gustos_categoria_tag.xml',

        #'views/reporte_personalizado.xml',
        #'views/view_gusto_informe_provincia.xml',
        #'views/gustos_gusto_sql.xml',

        #'views/gustos_contratos_informe.xml',
        #'views/gustos_datos.xml',
        #'views/gustos_objetivos.xml',
        #'views/gustos_listado_contratos_agrarios.xml',
        #'views/gustos_listado_contratos_genyaut.xml',
        #'views/gustos_objetivos2.xml',
        #'views/gustos_candidatos.xml',
        #
        #'views/gustos_formaciones.xml',
        #'views/gustos_tipo_formacion.xml',
        #'views/gustos_provisional.xml',
        #'data/notify_cron.xml',
        #'views/gustos_notify_message.xml',
        #'views/gustos_talleres_import_wizard.xml',
        # llamadas a formularios desde gusto
        
        'views/templates.xml',
        'views/inforef_menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
