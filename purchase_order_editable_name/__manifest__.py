{
    'name': 'Purchase Order Editable Name',
    'version' : '17.0',
    'summary': 'Makes the name field in purchase order editable',
    'sequence': 10,
    'description': """
Father (TOTP)
================================
Allows users to configure
    """,
    'category': 'Purchases',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base', 'purchase'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'views/purchase_order_views.xml',
    ],
    'license': 'LGPL-3',
}