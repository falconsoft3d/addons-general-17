{
    'name': 'Restringir Importación / Exportación',
    'version': '17.0.1.0.0',
    'summary': 'Controla quién puede importar y exportar datos en Odoo',
    'sequence': 10,
    'description': """
Restringir Importación / Exportación
=====================================
Permite al administrador habilitar o deshabilitar los permisos
de importación y exportación de datos para los usuarios.
    """,
    'category': 'Extra Tools',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base', 'base_setup'],
    'auto_install': False,
    'data': [
        'security/security.xml',
        'views/view.xml',
    ],
    'license': 'LGPL-3',
}