from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_allow_export = fields.Boolean(
        string='Permitir Exportación',
        implied_group='import_export.group_allow_export',
        help='Habilita la exportación de datos para todos los usuarios internos.',
    )
    group_allow_import = fields.Boolean(
        string='Permitir Importación',
        implied_group='import_export.group_allow_import',
        help='Habilita la importación de datos para todos los usuarios internos.',
    )
