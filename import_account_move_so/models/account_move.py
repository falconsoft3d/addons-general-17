# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    old_id = fields.Integer('Old ID', copy=False)
    import_account_move_id = fields.Many2one('import.account.move', 'Import Account Move', copy=False)