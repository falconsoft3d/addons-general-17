# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SequenceCancel(models.Model):
    _name = 'sequence.cancel'
    _rec_name = 'journal_id'

    journal_id = fields.Many2one('account.journal', 'Diario')
    move_type = fields.Selection(string='Tipo',  selection=[('inv', 'Factura'), ('ref', 'Rectificativa')])
    sequence_cancel_line_ids = fields.One2many('sequence.cancel.line', 'sequence_cancel_id', 'Secuncias')
    company_id = fields.Many2one('res.company', string='Compañía')

class SequenceCancelLine(models.Model):
    _name = 'sequence.cancel.line'
    _order = 'name asc'

    name = fields.Char('Secuencia')
    state = fields.Selection(selection=[('canceled', 'Anulado'),('assigned', 'Reasignado')], string='Status')
    sequence_cancel_id = fields.Many2one('sequence.cancel', 'Sequencia')

    def _verify_sequence_line_available(self):
        sequence = False
        if self.state == 'canceled':
            sequence = self.name
            self.state = 'assigned'
        return sequence