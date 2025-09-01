{
    'name': 'Account Move Payday MFH',
    'version' : '1.2',
    'summary': 'Invoices & Payments MFH',
    'sequence': 10,
    'description': """
Father (TOTP)
================================
Allows users to configure
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['account','payment_mode_show'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
    ],
    'license': 'LGPL-3',
}