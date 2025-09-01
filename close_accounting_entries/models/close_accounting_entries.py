# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import UserError


class CloseAccountingEntries(models.Model):
    _name = 'account.close.accounting.entries'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _description = 'Accounting Lock'
    _order = 'id desc'

    name = fields.Date(
        'From', required=True, tracking=True, default=fields.Date.today)
    date_to = fields.Date(
        'To', required=True, tracking=True, default=fields.Date.today)
    lock_modify_asset = fields.Boolean(
        'Not modify assets', default=True, tracking=True)
    lock_create_asset = fields.Boolean(
        'Not create assets', default=True, tracking=True)

    lock_stock = fields.Boolean(
        'Block stock', default=True, tracking=True)

    lock_accounting = fields.Boolean(
        'Block accounting', default=True, tracking=True
    )

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, readonly=True,
                                 default=lambda self: self.env.company)