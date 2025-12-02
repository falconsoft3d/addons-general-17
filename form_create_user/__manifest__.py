{
    'name': 'Form Create User MFH',
    'version': '1.0',
    'summary': 'Formulario público para auto-crear usuarios',
    'sequence': 10,
    'description': """
Formulario de Auto-Creación de Usuarios
========================================
Permite a usuarios públicos registrarse automáticamente:
- Formulario web público
- Creación automática de usuarios internos clonando un usuario plantilla
- Generación automática de oportunidades en CRM
- Muestra credenciales generadas al usuario
    """,
    'category': 'Extra Tools',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base', 'crm', 'website'],
    'auto_install': False,
    'data': [
        'data/ticketproo_config.xml',
        'views/view.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'form_create_user/static/src/css/form_styles.css',
        ],
    },
    'license': 'LGPL-3',
}