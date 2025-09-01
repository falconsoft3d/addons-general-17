# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_res_payment_document_id = fields.Many2one('res.payment.document', string='Payment Document')