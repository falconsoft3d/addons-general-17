from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('name', 'default_code')
    def _check_unique_name_and_code(self):
        """
        Restringe que no puedan existir dos productos con el mismo nombre
        y referencia interna (default_code).
        """
        for product in self:
            if product.default_code:
                existing_product = self.env['product.template'].search([
                    ('id', '!=', product.id),
                    ('name', '=', product.name),
                    ('default_code', '=', product.default_code),
                ], limit=1)

                if existing_product:
                    raise ValidationError(
                        f"Ya existe un producto con el nombre '{product.name}' "
                        f"y la referencia interna '{product.default_code}'."
                    )
            else:
                existing_product = self.env['product.template'].search([
                    ('id', '!=', product.id),
                    ('name', '=', product.name),
                ], limit=1)

                if existing_product:
                    raise ValidationError(
                        f"Ya existe un producto con el nombre '{product.name}'."
                    )
