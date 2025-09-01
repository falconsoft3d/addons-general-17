# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmProInfo(models.Model):
    _description = "Crm Pro Info"
    _name = 'crm.pro.info'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    email_title = fields.Char(string='Email Title', required=True)
    email_body = fields.Text(string='Email Body', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    send_email = fields.Boolean(string='Send Email', default=False)
    numer_days = fields.Integer(string='Number of Days', default=0)