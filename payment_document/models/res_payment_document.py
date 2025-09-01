# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import csv
import requests

class ResPaymentDocument(models.Model):
    _description = "Res Payment Document"
    _name = 'res.payment.document'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Char('Name', copy=False)
    code = fields.Char('Code')