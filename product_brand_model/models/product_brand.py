# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'

    name = fields.Char('Brand Name', required=True)
    description = fields.Text('Description', translate=True)
    code = fields.Char('Code', required=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Select a partner for this brand if any.',
        ondelete='restrict'
    )
    logo = fields.Binary('Logo File')
    product_ids = fields.One2many(
        'product.template',
        'product_brand_id',
        string='Products in this Brand',
    )
    products_count = fields.Integer(
        string='Number of Products',
        compute='_get_products_count',
    )

    @api.depends('product_ids')
    def _get_products_count(self):
        for record in self:
            record.products_count = len(record.product_ids)