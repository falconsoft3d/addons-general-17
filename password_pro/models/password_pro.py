# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PasswordPro(models.Model):
    _description = "Password Pro"
    _name = 'password.pro'
    _order = 'id desc'


    name = fields.Char('User')
    password = fields.Char('Password')
    model = fields.Char('Model')
    url = fields.Char('URL')