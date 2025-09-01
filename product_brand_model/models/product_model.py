# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductModel(models.Model):
    _name = 'product.model'
    _description = 'Product Brand Model'

    name = fields.Char('Model Name', required=True)
    description = fields.Text('Description', translate=True)
    brand_id = fields.Many2one('product.brand', string='Brand',ondelete='restrict', required=True)
    code = fields.Char('Code', required=True)
    logo = fields.Binary('Logo File')
