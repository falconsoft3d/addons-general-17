# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    list_price_tax = fields.Float(
        string="P.V.P",
        compute="_compute_list_price_tax",
        help="Price with tax",
    )


    @api.depends("list_price", "taxes_id")
    def _compute_list_price_tax(self):
        for record in self:
            if record.taxes_id:
                record.list_price_tax = record.list_price * (1 + sum(tax.amount for tax in record.taxes_id) / 100)
            else:
                record.list_price_tax = record.list_price