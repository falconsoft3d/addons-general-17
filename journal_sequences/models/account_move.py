# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('journal_id')
    def _onchange_journal(self):
        if self.move_type in ['out_invoice', 'in_invoice']:
            if self.journal_id.main_sequence_id and not self.name:
                self.name = '/'
        if self.move_type in ['out_refund', 'in_refund']:
            if self.journal_id.rect_sequence_id and not self.name:
                self.name = '/'

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        for move in self:
            if move.move_type in ['out_invoice', 'in_invoice']:
                if move.journal_id.main_sequence_id and not move.name:
                    move.name = '/'
            if move.move_type in ['out_refund', 'in_refund']:
                if move.journal_id.rect_sequence_id and not move.name:
                    move.name = '/'
            return super(AccountMove, self)._compute_name()

    def action_post(self):
        for move in self:
            if move.move_type in ['out_invoice', 'in_invoice']:
                if move.journal_id.main_sequence_id and move.name == '/':
                    sequence = move.journal_id.main_sequence_id._next_do()
                    move.name = sequence
            if move.move_type in ['out_refund', 'in_refund']:
                if move.journal_id.rect_sequence_id and move.name == '/':
                    sequence = move.journal_id.rect_sequence_id._next_do()
                    move.name = sequence
            return super(AccountMove, self).action_post()