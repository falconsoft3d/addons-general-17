{
    'name': 'SQL Report - MFH',
    'version': '17.0',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'description': """
Ticket Pro (TOTP)
================================
Allows users to configure
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base','mail'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'views/ir_sequence.xml',
        'security/group_security.xml',
        'security/ir.model.access.csv',
        'data/data_view.xml',
        'views/sql_report_view.xml'
        ],

        'installable': True,
        'application': False,
        'auto_install': False,
        'license': 'LGPL-3',
}
