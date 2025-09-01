{
    'name': 'Supplier Portal MFH',
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
    'depends': ['base','purchase'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'views/res_partner_views.xml',
    ],
    'license': 'LGPL-3',
}