# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_cost = fields.Float(compute='compute_picking_total_cost', store=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    use_standard_price = fields.Boolean(string='Usar Costo', default=False)
    use_demand = fields.Boolean(string='Usar Demanda', default=False)


    def action_update_total(self):
        for rec in self:
            rec.update_picking_total_cost()


    @api.depends('move_ids_without_package.product_cost','move_ids_without_package.quantity')
    def compute_picking_total_cost(self):
        _logger.info('= compute_picking_total_cost = ')
        for picking in self:
            total = 0
            for line in picking.move_ids_without_package:
                if picking.use_demand:
                    total += line.product_cost * ( line.product_uom_qty - line.assets_qty )
                else:
                    total += line.product_cost * ( line.quantity - line.assets_qty )
            picking.total_cost = total

    def update_picking_total_cost(self):
        _logger.info('= begin update_picking_total_cost = ')
        _logger.info('= purchase_id = %s', self.purchase_id)
        for picking in self:
            for line in picking.move_ids_without_package:
                if self.state == 'done':
                    line.assets_qty = 0

                if not picking.use_standard_price:
                    _logger.info('not picking.use_standard_price')
                    _logger.info('= purchase_id => %s', self.purchase_id)
                    if self.purchase_id:
                        line.purchase_id = self.purchase_id.id
                        product_cost = line._find_purchase_price(self.purchase_id)

                        _logger.info('= product_cost => %s', product_cost)
                        line.product_cost = product_cost if product_cost > 0 else line.product_id.standard_price
                    else:
                        if line.purchase_id:
                            product_cost = line._find_purchase_price(line.purchase_id)
                            line.product_cost = product_cost if product_cost > 0 else line.product_id.standard_price
                else:
                    _logger.info('yes picking.use_standard_price')
                    line.product_cost = line.product_id.standard_price

            picking.compute_picking_total_cost()

        _logger.info('= end update_picking_total_cost = ')

class StockMove(models.Model):
    _inherit = 'stock.move'
    product_cost = fields.Float()
    purchase_id = fields.Many2one('purchase.order')
    assets_qty = fields.Float(string='Assets Qty')
    subtotal = fields.Float(compute='compute_subtotal')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')


    def compute_subtotal(self):
        for move in self:
            if move.picking_id and move.picking_id.use_demand:
                move.subtotal = move.product_cost * ( move.product_uom_qty - move.assets_qty )
            else:
                move.subtotal = move.product_cost * ( move.quantity - move.assets_qty )

    @api.model
    def create(self, vals):
        move = super().create(vals)
        if move.product_id:
            move.product_cost = move.product_id.standard_price
        if move.purchase_id:
            price = move._find_purchase_price(move.purchase_id)
            if price > 0:
                move.product_cost = price
        elif move.product_id and move.picking_id and move.picking_id.purchase_id:
            price = move._find_purchase_price(move.picking_id.purchase_id)
            if price > 0:
                move.product_cost = price
        return move

    def _find_purchase_price(self, purchase_id):
        _logger.info('= _find_purchase_price = ')
        _logger.info('= purchase_id => %s', purchase_id.id)
        price = 0
        purchase_lines = purchase_id.order_line.filtered_domain([('product_id','=', self.product_id.id)])
        if purchase_lines:
            if purchase_lines[0].discount > 0:
                price = purchase_lines[0].price_unit * (1 - (purchase_lines[0].discount / 100))
            else:
                price = purchase_lines[0].price_unit
        return price