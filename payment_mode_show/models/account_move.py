# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('needed_terms', 'invoice_payment_term_id', 'invoice_date')
    def _compute_invoice_date_due(self):
        for record in self:
            if record.state == 'draft' or not record.invoice_date_due:
                today = fields.Date.context_today(record)
                for move in record:
                    move.invoice_date_due = move.needed_terms and max(
                        (k['date_maturity'] for k in move.needed_terms.keys() if k),
                        default=False,
                    ) or move.invoice_date_due or today



