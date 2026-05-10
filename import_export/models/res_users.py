from odoo import fields, models, Command


class ResUsers(models.Model):
    _inherit = 'res.users'

    allow_export = fields.Boolean(
        string='Permitir Exportación',
        compute='_compute_allow_export',
        inverse='_set_allow_export',
    )
    allow_import = fields.Boolean(
        string='Permitir Importación',
        compute='_compute_allow_import',
        inverse='_set_allow_import',
    )

    def _compute_allow_export(self):
        group = self.env.ref('import_export.group_allow_export')
        for user in self:
            user.allow_export = group in user.groups_id

    def _set_allow_export(self):
        group = self.env.ref('import_export.group_allow_export')
        for user in self:
            if user.allow_export:
                group.write({'users': [Command.link(user.id)]})
            else:
                group.write({'users': [Command.unlink(user.id)]})

    def _compute_allow_import(self):
        group = self.env.ref('import_export.group_allow_import')
        for user in self:
            user.allow_import = group in user.groups_id

    def _set_allow_import(self):
        group = self.env.ref('import_export.group_allow_import')
        for user in self:
            if user.allow_import:
                group.write({'users': [Command.link(user.id)]})
            else:
                group.write({'users': [Command.unlink(user.id)]})
