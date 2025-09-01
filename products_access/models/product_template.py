# coding: utf-8
from lxml import etree
from odoo import api, models, _
from odoo.exceptions import UserError,ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not self.env.user.product_access:
                raise UserError(_("Usuario no autorizado para crear productos."))
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.user.product_access:
            raise UserError(_("Usuario no autorizado para editar productos."))
        return super(ProductTemplate, self).write(vals)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not self.env.user.product_access:
                raise UserError(_("Usuario no autorizado para crear productos."))
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.user.product_access:
            raise UserError(_("Usuario no autorizado para editar productos."))
        return super(ProductProduct, self).write(vals)
