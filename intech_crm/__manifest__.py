# -*- coding: utf-8 -*-
{
    'name': "Intech CRM",
    'author': 'SNine',
    'company': 'SNine',
    'maintainer': 'SNine',
    'website': "https://www.snine.vn",
    'category': 'CRM',
    'version': '0.1',
    'depends': ['base', 'crm', 'sale', 'sales_team'],
    'data': [
        'security/crm_security.xml',
        'security/rule_crm.xml',
        'security/ir.model.access.csv',

        'views/crm_data_view.xml',
        'views/crm_lead_views.xml',
        'views/res_partner_views.xml',
        'views/crm_team_views.xml',
        'views/menu_item.xml',

        'data/sequence_code_partner.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'intech_crm/static/src/**/*.css',
            'intech_crm/static/src/views/**/*.xml',
            'intech_crm/static/src/views/**/*.js',
        ],
    },
    "installable": True,
    'application': True,
    'license': 'LGPL-3',
    'post_init_hook': 'post_init_hook_remove_rule_core_crm',
    'uninstall_hook': 'uninstall_hook_setup_rule_core_crm'
}
