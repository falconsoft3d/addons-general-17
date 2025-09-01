{
    'name': 'Import Account Move Soltec MFH',
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
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'views/import_account_move_views.xml',
        'views/account_move_views.xml',
    ],
    'license': 'LGPL-3',
}