# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_cancelled_folio = fields.Boolean(string='Is_cancelled_folio')

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        for move in self:
            if move.move_type in ['out_invoice', 'in_invoice']:
                if move.journal_id.main_sequence_id and move.name == '':
                    move.name = '/'
            if move.move_type in ['out_refund', 'in_refund']:
                if move.journal_id.rect_sequence_id and move.name == '':
                    move.name = '/'
            return super(AccountMove, self)._compute_name()

    def action_post(self):
        seq_cancel_obj = self.env['sequence.cancel']
        for move in self:
            sequence = move.name
            if move.move_type in ['out_invoice', 'in_invoice']:
                seq_cancel = seq_cancel_obj.search([('journal_id', '=', self.journal_id.id),('move_type','=','inv')])
                if move.is_cancelled_folio:
                    move.name = '/'
                    move.payment_reference = ''
                if move.journal_id.main_sequence_id:
                    assigned = False
                    if move.name == '/':
                        if seq_cancel:
                            for line in seq_cancel.sequence_cancel_line_ids:
                                sequence = line._verify_sequence_line_available()
                                if sequence:
                                    assigned = True
                                    self._notify_cancelled_folio(sequence)
                                    break
                        else:
                            assigned = False
                    if not assigned and move.name == '/':
                        sequence = move.journal_id.main_sequence_id._next_do()
                    move.name = sequence
                    move.payment_reference = sequence
                    move.is_cancelled_folio = False
            if move.move_type in ['out_refund', 'in_refund']:
                seq_cancel = seq_cancel_obj.search([('journal_id', '=', self.journal_id.id), ('move_type', '=', 'ref')])
                if move.is_cancelled_folio:
                    move.name = '/'
                    move.payment_reference = ''
                if move.journal_id.rect_sequence_id:
                    assigned = False
                    if move.name == '/':
                        if seq_cancel:
                            for line in seq_cancel.sequence_cancel_line_ids:
                                sequence = line._verify_sequence_line_available()
                                if sequence:
                                    assigned = True
                                    self._notify_cancelled_folio(sequence)
                                    break
                        else:
                            assigned = False
                    if not assigned and move.name == '/':
                        sequence = move.journal_id.rect_sequence_id._next_do()
                    move.name = sequence
                    move.payment_reference = sequence
                    move.is_cancelled_folio = False
        return super(AccountMove, self).action_post()

    def _aux_create_cancel_line(self,seq_cancel_line_obj,seq_cancel,name):
        vals = self._prepare_seq_cancel_line_vals(seq_cancel,name)
        new_seq_line = seq_cancel_line_obj.create(vals)
        return new_seq_line

    def _prepare_seq_cancel_line_vals(self,seq_cancel,name):
        vals = {
            'name': name,
            'state': 'canceled',
            'sequence_cancel_id': seq_cancel.id,
        }
        return vals

    def button_cancel_folio(self):
        seq_cancel_obj = self.env['sequence.cancel']
        seq_cancel_line_obj = self.env['sequence.cancel.line']
        for record in self:
            name = record.name
            journal = record.journal_id
            if record.move_type in ['out_invoice', 'in_invoice']:
                move_type = 'inv'
            if record.move_type in ['out_refund', 'in_refund']:
                move_type = 'ref'
            seq_cancel = seq_cancel_obj.search([('journal_id', '=', journal.id), ('move_type', '=', move_type)])
            if seq_cancel:
                add_line = True
                for line in seq_cancel.sequence_cancel_line_ids:
                    if name == line.name:
                        line.state = 'canceled'
                        add_line = False
                        record.name = False
                        record.posted_before = False
                        record.payment_reference = ''
                        record.is_cancelled_folio = True
                        break
                    # else:
                    #     add_line = True
                if add_line:
                    seq_line = self._aux_create_cancel_line(seq_cancel_line_obj,seq_cancel,name)
                    record.name = False
                    record.posted_before = False
                    record.payment_reference = ''
                    record.is_cancelled_folio = True
                    _logger.info('Creado nuevo folio anulado para el diario %s (%s)' % (journal.name, seq_line.name))
            else:
                line = []
                vals_line = {
                    'name': name,
                    'state': 'canceled',
                }
                line.append((0, 0, vals_line))
                vals = {
                    'journal_id': journal.id,
                    'move_type': move_type,
                    'company_id': journal.company_id.id,
                    'sequence_cancel_line_ids': line
                }
                seq_cancel_new = seq_cancel_obj.create(vals)
                record.name = False
                record.payment_reference = ''
                record.posted_before = False
                record.is_cancelled_folio = True
                _logger.info('Creado nuevo listado de folios para el diario %s (%s)' % (journal.name, seq_cancel_new))

    def _notify_cancelled_folio(self, folio):
        subject = f"Tomado folio anulado {folio}"

        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'type': 'success',
            'title': '',
            'message': subject,
        })

        self.message_post(body=subject)