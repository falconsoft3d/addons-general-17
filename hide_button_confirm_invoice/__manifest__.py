{
    'name': 'Hide Button Confirm Invoice MFH',
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
    'depends': ['base','account'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'security/security.xml',
        'views/account_move_views.xml',
    ],
    'license': 'LGPL-3',
}