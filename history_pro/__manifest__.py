{
    'name': 'History Pro MFH',
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
    'depends': ['base','mail', 'product', 'account'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/invoice_history_pro_views.xml',
        'views/menu_views.xml',
    ],
    'license': 'LGPL-3',
}