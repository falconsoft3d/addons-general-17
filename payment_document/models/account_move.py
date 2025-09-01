# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_res_payment_document_id = fields.Many2one('res.payment.document')

    @api.onchange('partner_id')
    def document_onchange_partner_id(self):
        if self.partner_id and not self.customer_res_payment_document_id:
            self.customer_res_payment_document_id = self.partner_id.customer_res_payment_document_id.id


    @api.constrains('state')
    def check_state(self):
        if self.partner_id and not self.customer_res_payment_document_id:
            self.customer_res_payment_document_id = self.partner_id.customer_res_payment_document_id.id