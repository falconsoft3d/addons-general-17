# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ProductSerial(models.Model):
    _name = 'product.serial'
    _description = 'Product Serial'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description', translate=True)
    model_id = fields.Many2one('product.model', string='Model',ondelete='restrict', required=True)
    code = fields.Char('Code', required=True)
    logo = fields.Binary('Logo File')
