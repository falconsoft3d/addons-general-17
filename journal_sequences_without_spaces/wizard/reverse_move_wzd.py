# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
class ReverseMove(models.TransientModel):
    _inherit = 'account.move.reversal'

    def reverse_moves(self, is_modify=False):
        res = super().reverse_moves(is_modify=is_modify)
        if not is_modify:
            if 'res_id' in res:
                refund = self.env['account.move'].browse(res['res_id'])
                self._helper_assign_folios(refund)
            elif 'domain' in res:
                refunds = self.env['account.move'].search(res['domain'])
                self._helper_assign_folios(refunds)

        return res

    def _helper_assign_folios(self, refunds):
        folio_obj = self.env['sequence.cancel.line']
        for refund in refunds:
            folio_line = folio_obj.search(
                [('state', '=', 'canceled'), ('sequence_cancel_id.journal_id', '=', refund.journal_id.id)], limit=1)
            if folio_line:
                folio_line.state = 'assigned'
                refund.name = folio_line.name