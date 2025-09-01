# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SequenceCancelLine(models.Model):
    _inherit = 'sequence.cancel.line'

    company_working_year_id = fields.Many2one('company.working.year', string='Año')

    def _verify_sequence_line_available(self):
        sequence = False
        if self.state == 'canceled' and self.company_working_year_id == self.env.user.company_working_year_id:
            sequence = self.name
            self.state = 'assigned'
        return sequence