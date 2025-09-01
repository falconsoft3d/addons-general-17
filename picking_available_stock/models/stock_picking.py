from odoo import models, api, fields, _

import logging
_logger = logging.getLogger(__name__)



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.onchange("location_id")
    def _compute_products_stock(self):
        for picking in self:
            for move in picking.move_ids_without_package:
                move.qty_available_location = move.product_id.with_context(
                    location=picking.location_id.id
                ).qty_available



class StockMove(models.Model):
    _inherit = 'stock.move'
    # move_ids_without_package    # move_ids

    qty_available_location = fields.Float(readonly=True, string="Qty Available in Location")


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    # move_line_ids_without_package      # move_line_ids,