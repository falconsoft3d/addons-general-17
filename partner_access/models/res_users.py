# coding: utf-8
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'
    partner_access = fields.Boolean('Acceso a Contactos', default=True)
