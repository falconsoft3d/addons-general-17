{
    'name': 'Permitir Archivar',
    'version': '17.0.1.0.0',
    'summary': 'Controla quién puede archivar registros mediante un permiso de usuario',
    'sequence': 10,
    'description': """
Permitir Archivar
=================
Agrega el permiso "Permitir Archivar" en los usuarios.
Si un usuario no tiene este permiso, no puede archivar
ni desarchivar ningún registro en el sistema.
    """,
    'category': 'Extra Tools',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base'],
    'auto_install': False,
    'data': [
        'security/security.xml',
        'views/view.xml',
    ],
    'license': 'LGPL-3',
}