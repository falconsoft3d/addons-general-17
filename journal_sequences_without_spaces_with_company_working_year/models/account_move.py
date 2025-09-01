# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _prepare_seq_cancel_line_vals(self,seq_cancel,name):
        vals = super()._prepare_seq_cancel_line_vals(seq_cancel,name)
        vals.update({
            'company_working_year_id': self.env.user.company_working_year_id.id
        })
        return vals

