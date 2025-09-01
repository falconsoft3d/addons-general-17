{
    'name': 'Invoice to account MFH',
    'version' : '1.2',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'description': """
Invoice to account
================================
Allows users to configure
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base','account'],
    'external_dependencies': {
        'python': ['invoice2data'],
    },
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'data/ir_cron.xml',
    ],
    'license': 'LGPL-3',
}