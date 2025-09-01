{
    'name': 'Employee Courses MFH',
    'version' : '1.2',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'description': """
Father (TOTP)
================================
Allows users to configure
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base','hr','mail'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/employee_courses_views.xml',
        'views/course_taken_views.xml',
        'views/hr_employee_views.xml',
        'views/menu_views.xml',
    ],
    'license': 'LGPL-3',
}