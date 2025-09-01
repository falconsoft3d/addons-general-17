# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class DirectoryPartner(models.Model):
    _description = "Directory Partner"
    _name = 'directory.partner'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Char('Nombre')
    phone = fields.Char('Teléfono')
    email = fields.Char('Correo')
    cargo = fields.Char('Cargo')
    partner_id = fields.Many2one('res.partner', string='Empresa')