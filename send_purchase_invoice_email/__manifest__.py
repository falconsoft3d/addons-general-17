{
    'name': 'Send Purchase Invoice MFH',
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
    'depends': ['account', 'purchase', 'mail'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'data/mail_template_data.xml',
        'views/account_move_views.xml',
    ],
    'license': 'LGPL-3',
}