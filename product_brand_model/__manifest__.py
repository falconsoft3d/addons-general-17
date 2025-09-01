{
    'name': 'Product Brand & Model MFH',
    'version' : '1.2',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'description': """
Product Brand & Model
================================
Allows users to configure product brands and models.
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base','product','sale'],
    'category': 'Products',
    'auto_install': False,
    'data': [
        'views/product_brand_views.xml',
        'views/product_model_views.xml',
        'views/product_serial_views.xml',
        'views/product_views.xml',
        'views/menu_views.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'LGPL-3',
}