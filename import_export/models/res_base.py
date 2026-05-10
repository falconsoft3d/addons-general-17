from odoo import api, models, _
from odoo.exceptions import AccessError


class Base(models.AbstractModel):
    _inherit = 'base'

    def export_data(self, fields_to_export):
        if not self.env.is_superuser() and \
                not self.env.user.has_group('import_export.group_allow_export'):
            raise AccessError(_('No tiene permiso para exportar datos.'))
        return super().export_data(fields_to_export)

    @api.model
    def load(self, fields, data):
        if not self.env.is_superuser() and \
                not self.env.user.has_group('import_export.group_allow_import'):
            raise AccessError(_('No tiene permiso para importar datos.'))
        return super().load(fields, data)
