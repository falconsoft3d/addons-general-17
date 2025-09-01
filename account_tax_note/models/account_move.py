# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    tax_note = fields.Text(string='Nota en el Impuesto' , compute='_compute_tax_note', store=True)

    @api.depends('line_ids', 'amount_total')
    def _compute_tax_note(self):
        for move in self:
            if move.line_ids:
                if move.line_ids[0].tax_ids:
                    move.tax_note =  move.line_ids[0].tax_ids[0].tax_note
                else:
                    move.tax_note = ''
            else:
                move.tax_note = ''