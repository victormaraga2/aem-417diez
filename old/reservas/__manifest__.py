# -*- coding: utf-8 -*-
{
    'name': "reservas",

    'summary': """
        Gestión para la reservas de aulas""",

    'description': """
        Gestión para la reservass de aulas
    """,

    'author': "Centro Tecnoformación",
    'website': "https://tecno-formacion.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'crm', 'inforef','stock', 'project'],

    'assets': {
    'web.assets_backend': [
         #'gusto/static/src/css/captacion.css',  
         'reservas/static/description/Logo-odoo.png',   
    ],
    },
    'installable': True,
    'application': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/reservas_aula.xml',
        'views/reservas_menu.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
