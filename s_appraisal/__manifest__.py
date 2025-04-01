# -*- coding: utf-8 -*-

{
    'name': "S-Appraisal",
    'author': 'SNine',
    'company': 'SNine',
    'maintainer': 'SNine',
    'website': "https://snine.vn",
    'category': 'Uncategorized',
    'version': '1.2',
    'depends': ['base', 'web', 'mail', 'hr_appraisal', 'hr_appraisal_survey', 'survey'],
    'data': [
        'security/hr_appraisal_survey_security.xml',
        'security/ir.model.access.csv',
        'views/hr_appraisal_views.xml',
        'views/appraisal_ask_feedback_views.xml',
        'views/survey_templates.xml',
        'views/survey_user_input_views.xml',
        'views/survey_user_views.xml',
        'views/survey_templates_management.xml',
        'views/survey_templates_print.xml',
        'data/hr_appraisal_templates.xml',

    ],
    'assets': {
        'web.assets_backend': [
            's_appraisal/static/src/**/*',
        ]
    },
    "price": 5,
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
