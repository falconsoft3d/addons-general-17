# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    main_sequence_id = fields.Many2one('ir.sequence', 'Secuencia principal')
    rect_sequence_id = fields.Many2one('ir.sequence', 'Secuencia rectificativa')