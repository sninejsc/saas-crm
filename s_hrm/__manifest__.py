# -*- coding: utf-8 -*-
{
    'name': "S-HRM",
    'author': 'SNine',
    'company': 'SNine',
    'maintainer': 'SNine',
    'website': "https://snine.vn",
    'category': 'HRM',
    'version': '0.1',
    'depends': ['base', 'room', 'mail', 'hr_org_chart','hr_holidays', 'hr_skills', 'hr_contract', 'web', 'hr',
                'base_import', 'hr_expense', 'analytic', 'project', 'hr_timesheet', 'timesheet_grid','hr_timesheet_attendance',
                'resource'],
    'data': [
        'data/sequence_code_employee.xml',

        'security/security_rules.xml',
        'security/ir.model.access.csv',

        'views/favicon.xml',
        'views/hr_employee_views.xml',
        'views/hr_expense_views.xml',
        'views/room_room_views.xml',
        'views/room_booking_views.xml',
        'views/room_booking_menus.xml',
        'views/hr_org_chart_views.xml',
        'views/hr_resume_line_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_leave_allocation_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'intech_hrm/static/src/css/intech_hrm.css',
            'intech_hrm/static/src/css/dropdown.scss',
            'intech_hrm/static/src/js/dropdown.js',
            'intech_hrm/static/src/js/dropdown.xml',
            'intech_hrm/static/src/js/title_soon.js',
            'intech_hrm/static/src/view/import_data_content.xml',
            'intech_hrm/static/src/view/datetime_picker_popover.xml',
        ]
    },
    "price": 5,
    'images': ['static/description/banner.png'],
    "installable": True,
    'application': True,
    'post_init_hook': 'post_init_hook_remove_rule_core_hrm',
    'uninstall_hook': 'uninstall_hook_setup_rule_core_hrm',
    'license': 'LGPL-3',
}
