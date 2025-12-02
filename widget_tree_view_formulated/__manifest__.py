{
    'name': 'Tree View Formulated Widget',
    'version': '17.0.1.0.0',
    'summary': 'Custom widget for tree views with formula-based totals',
    'sequence': 10,
    'description': """
Tree View Formulated Widget
================================
Permite definir fórmulas personalizadas en Python para calcular totales en vistas tree.
Cada columna puede tener su propia fórmula usando el atributo options="{'formulated': 'formula'}".

Características:
- Fórmulas personalizadas por columna
- Reemplazo automático de sumas por defecto
- Soporte para operaciones matemáticas complejas
- Compatible con campos numéricos y monetarios
    """,
    'category': 'Extra Tools',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['web'],
    'data': [
        'views/view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'widget_tree_view_formulated/static/src/css/tree_view_formulated.css',
            'widget_tree_view_formulated/static/src/js/tree_view_formulated.js',
        ],
    },
    'auto_install': False,
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}