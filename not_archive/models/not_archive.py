from odoo import models, _
from odoo.exceptions import UserError


class Base(models.AbstractModel):
    _inherit = 'base'

    def action_archive(self):
        if not self.env.user.has_group('not_archive.group_can_archive'):
            raise UserError(_(
                'No tiene permiso para archivar registros. '
                'Contacte a su administrador para obtener el permiso "Permitir Archivar".'
            ))
        return super().action_archive()

    def action_unarchive(self):
        if not self.env.user.has_group('not_archive.group_can_archive'):
            raise UserError(_(
                'No tiene permiso para desarchivar registros. '
                'Contacte a su administrador para obtener el permiso "Permitir Archivar".'
            ))
        return super().action_unarchive()
