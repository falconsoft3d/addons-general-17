from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move'

    check_consume = fields.Boolean(
        compute='_compute_check_consume',
        store=True,  # si quieres que se guarde en la DB
        string='Check consume',
        default=False,
    )

    @api.depends('product_id')
    def _compute_check_consume(self):
        for rec in self:
            rec.check_consume = bool(rec.product_id.check_consume)


