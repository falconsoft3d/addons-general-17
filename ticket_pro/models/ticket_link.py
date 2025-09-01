# -*- coding: utf-8 -*-
from odoo import api, fields, models


class TicketLink(models.Model):
    _description = "Ticket Link"
    _name = 'ticket.link'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'
    name = fields.Char('Nombre', copy=False)
    link = fields.Char('Link', copy=False)