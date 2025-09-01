# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand_id = fields.Many2one(
        'product.brand',
        string='Brand',
        help='Select a brand for this product.',
    )

    model_id = fields.Many2one('product.model', string='Model')
    serial_id = fields.Many2one('product.serial', string='Serial')


    @api.onchange('product_brand_id')
    def _onchange_product_brand_id(self):
        self.model_id = False
        return {'domain': {'model_id': [('brand_id', '=', self.product_brand_id.id)]}}


    @api.onchange('model_id')
    def _onchange_model_id(self):
        self.serial_id = False
        return {'domain': {'serial_id': [('model_id', '=', self.model_id.id)]}}

