# coding: utf-8
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'
    product_access = fields.Boolean('Acceso a Productos',default=True)
