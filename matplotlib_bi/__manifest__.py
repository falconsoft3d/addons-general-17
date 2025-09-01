{
    'name': 'Matplotlib BI MFH',
    'version' : '1.2',
    'summary': 'Matplotlib',
    'sequence': 10,
    'description': """
Matplotlib BI
================================
Allows users to configure BI reports using Matplotlib.
    """,
    'category': 'BI/BI',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base'],
    'category': 'Extra Tools',
    'external_dependencies': {
        'python': ['matplotlib'],
    },
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/matplotlib_bi_views.xml',
    ],
    'license': 'LGPL-3',
}