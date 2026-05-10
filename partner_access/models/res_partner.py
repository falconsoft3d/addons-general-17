# coding: utf-8
from odoo import api, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not self.env.user.partner_access:
                raise UserError(_("Usuario no autorizado para crear contactos."))
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.user.partner_access:
            raise UserError(_("Usuario no autorizado para editar contactos."))
        return super(ResPartner, self).write(vals)
