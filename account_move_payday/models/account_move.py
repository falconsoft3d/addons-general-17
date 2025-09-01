# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    payday = fields.Char(string='Payday')

    @api.onchange('partner_id')
    def payday_onchange_partner_id(self):
        for record in self:
            if record.partner_id and not record.payday:
                record.payday = record.partner_id.payday


    @api.constrains('state')
    def payday_check_state(self):
        for record in self:
            if record.partner_id and not record.payday:
                record.payday = record.partner_id.payday