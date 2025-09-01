# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class InvoiceHistoryPro(models.Model):
    _description = "Invoice History Pro"
    _name = 'invoice.history.pro'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner', string='Partner')
    invoice_date = fields.Date('Date')
    date = fields.Date('Date')
    old_id = fields.Integer('Old ID')
    user_id = fields.Many2one('res.users', string='User')
    currency_id = fields.Many2one('res.currency', string='Currency')
    amount_untaxed = fields.Monetary('Untaxed Amount')
    amount_tax = fields.Monetary('Tax Amount')
    amount_total = fields.Monetary('Total Amount')
    company_id = fields.Many2one('res.company', string='Company')
    narration = fields.Text('Notes')

    type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Vendor Bill'),
        ('out_refund', 'Customer Refund'),
        ('in_refund', 'Vendor Refund'),
        ('other', 'Other'),
    ], string='Type')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], string='Status')

    invoice_line_ids = fields.One2many('invoice.history.pro.line', 'invoice_id', string='Lines')


class InvoiceHistoryProLine(models.Model):
    _description = "Invoice History Pro Line"
    _name = 'invoice.history.pro.line'

    name = fields.Many2one('product.product', string='Product')
    invoice_id = fields.Many2one('invoice.history.pro', string='Invoice')
    quantity = fields.Float('Quantity')
    price_unit = fields.Monetary('Unit Price')
    discount = fields.Float('Discount (%)')
    amount_untaxed = fields.Monetary('Untaxed Amount')
    amount_tax = fields.Monetary('Tax Amount')
    amount_total = fields.Monetary('Total Amount')
    currency_id = fields.Many2one('res.currency', string='Currency', related='invoice_id.currency_id')
    company_id = fields.Many2one('res.company', string='Company', related='invoice_id.company_id')
    partner_id = fields.Many2one('res.partner', string='Partner', related='invoice_id.partner_id')
    date = fields.Date('Date', related='invoice_id.date')