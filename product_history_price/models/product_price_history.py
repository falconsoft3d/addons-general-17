# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductPriceHistory(models.Model):
    _name = 'product.price.history'
    _description = 'Histórico de Precios de Producto'
    _order = 'change_date desc, id desc'

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Producto',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Usuario',
        required=True,
        default=lambda self: self.env.user
    )
    
    change_date = fields.Datetime(
        string='Fecha',
        required=True,
        default=fields.Datetime.now
    )
    
    standard_price = fields.Float(
        string='Coste',
        digits='Product Price'
    )
    
    list_price = fields.Float(
        string='Precio de Venta',
        digits='Product Price'
    )
