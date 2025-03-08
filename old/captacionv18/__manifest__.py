# -*- coding: utf-8 -*-
{
    'name': "Captacion v18",

    'summary': """
        Modulo de captación de participantes a diferentes
        proyectos y programas de entidades""",

    'description': """
        Modulo de captación de participantes a diferentes
        proyectos y programas de entidades
    """,

    'author': "tecnoformacion",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'mail'],

    # always loaded
    'data': [
        'security/captacion_gestion_grupos.xml',
        'security/ir.model.access.csv',
        #'views/capta_experiencialaboral.xml',
        #'views/captacion_experiencialaboral.xml',
        
        'views/captacion_interesesprofesionales.xml',
        'views/captacion_productos.xml',
        'views/captacion_necesidadesformacionespecifica.xml',
        'views/captacion_objetivoprofesional.xml',
        'views/captacion_participantes.xml',
        'views/captacion_proyectos.xml',
        'views/captacion_programas.xml',
        'views/captacion_convocatorias.xml',
        'views/captacion_oportunidad.xml',
        

        
        #'security/ir.model.access.orientacion.csv',

        'views/captacion_gusto.xml',
        'views/captacion_acciones_formativas.xml',
        'views/captacion_talleres.xml',
        'views/captacion_contratos.xml',
        'views/captacion_contratos_sum.xml',
        'views/captacion_prospectores.xml',
        'views/captacion_formadores.xml',

        # NECESARIAS
        'views/captacion_docaem.xml',
        'views/captacion_fileviewer.xml',
        'views/captacion_historico_sto.xml',
        'views/captacion_view_form_captacion_talleres_creation.xml',
        'views/captacion_view_form_captacion_contratos_creation.xml',
        'views/captacion_confirm_docaem_wizard.xml',
        'views/captacion_docaem_confirm_wizard.xml',

        # PARAMETRICAS
        'views/captacion_docentes.xml',
        'views/captacion_accionformativa.xml',
        'views/captacion_colectivo.xml',
        'views/captacion_perfilocupacion.xml',
        'views/captacion_sectorocupacion.xml',
        'views/captacion_jornada.xml',
        'views/captacion_taller.xml',
        'views/captacion_tipo_doc.xml',
        
        #'views/captacion_docentes_acciones.xml',
        #'views/captacion_perfiles_participantes.xml',
        #'views/captacion_tipo_documento.xml',
        'views/captacion_tag.xml',
        'views/captacion_tipo_tag.xml',
        'views/captacion_categoria_tag.xml',

        #'views/reporte_personalizado.xml',
        'views/view_captacion_informe_provincia.xml',
        'views/captacion_captacion_sql.xml',

        'views/captacion_contratos_informe.xml',
        'views/captacion_datos.xml',
        'views/captacion_objetivos.xml',
        'views/captacion_listado_contratos_agrarios.xml',
        'views/captacion_listado_contratos_genyaut.xml',
        #'views/captacion_objetivos2.xml',
        #'views/captacion_candidatos.xml',
        #
        #'views/captacion_formaciones.xml',
        #'views/captacion_tipo_formacion.xml',
        #'views/captacion_provisional.xml',
        #'data/notify_cron.xml',
        #'views/captacion_notify_message.xml',
        #'views/captacion_talleres_import_wizard.xml',
        # llamadas a formularios desde captacion
        
        # 'views/menus.xml',
        #'views/views.xml',
        'views/captacion_menu.xml',
        'views/templates.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
