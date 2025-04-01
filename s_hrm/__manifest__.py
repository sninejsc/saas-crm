# -*- coding: utf-8 -*-
{
    'name': "S-HRM",
    'author': 'SNine',
    'company': 'SNine',
    'maintainer': 'SNine',
    'website': "https://snine.vn",
    'category': 'HRM',
    'version': '0.1',
    'depends': ['base', 'room', 'mail',
                'hr_holidays', 'hr_skills', 'hr_contract', 'web', 'hr'],
    'data': [
        'data/sequence_code_employee.xml',
        'security/security_rules.xml',
        'security/ir.model.access.csv',

        'views/favicon.xml',
        'views/hr_employee_views.xml',
        'views/room_room_views.xml',
        'views/room_booking_views.xml',
        'views/room_booking_menus.xml',
        'views/hr_org_chart_views.xml',
        'views/hr_leave_views.xml',
        'views/hr_resume_line_views.xml',
        'views/hr_leave_views.xml',
        'views/menu_views.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'intech_hrm/static/src/css/intech_hrm.css',
            'intech_hrm/static/src/css/dropdown.scss',
            'intech_hrm/static/src/js/dropdown.js',
            'intech_hrm/static/src/js/dropdown.xml',
            'intech_hrm/static/src/js/title_soon.js',
        ]
    },
    "price": 5,
    'images': ['static/description/banner.png'],
    "installable": True,
    'application': True,
    'license': 'LGPL-3',
}
