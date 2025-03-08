# -*- coding: utf-8 -*-
{
    'name': "infocap",

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
        'security/infocap_gestion_grupos.xml',
        'security/ir.model.access.csv',
        #'security/ir.model.accessres.csv',
        # 'security/ir.model.access.orientacion.csv',

        
        
        #'views/infocap_talleres.xml',
        #'views/gustos_contratos.xml',
        #'views/gustos_contratos_sum.xml',
        #'views/infocap_dinamizadores.xml',
        #'views/infocap_empresas_formadoras.xml',
        #'views/gustos_formadores.xml',

        'views/infocap_interesesprofesionales.xml',
        'views/infocap_productos.xml',
        'views/infocap_necesidadesformacionespecifica.xml',
        'views/infocap_objetivoprofesional.xml',
        'views/infocap_participantes.xml',
        'views/infocap_proyectos.xml',
        'views/infocap_programas.xml',
        'views/infocap_convocatorias.xml',
        'views/infocap_solicitudes.xml',
        'views/infocap_ediciones.xml',
        'views/infocap_acciones_formativas.xml',

        # PARAMETRICAS
        'views/infocap_docentes.xml',
        'views/infocap_colectivo.xml',
        'views/infocap_sectorocupacion.xml',
        'views/infocap_situacion.xml',
        'views/infocap_perfilocupacion.xml',
        #'views/infocap_tipo_jornada.xml',
        'views/infocap_tipo_documento.xml',
        'views/infocap_tipo_taller.xml',
        'views/infocap_tipo_accionformativa.xml',
        'views/infocap_fileviewer.xml',
        'views/infocap_solicitante_upload_form.xml',
        

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
        'views/infocap_menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
