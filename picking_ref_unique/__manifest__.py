{
    'name': 'Unique Stock Picking Name',
    'version' : '17.0',
    'summary': 'Ensure unique stock.picking ref before validation',
    'sequence': 10,
    'description': """
Father (TOTP)
================================
Allows users to configure
    """,
    'category': 'Inventory',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base', 'stock','picking_supplier_reference'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'views/view.xml',
    ],
    'license': 'LGPL-3',
}