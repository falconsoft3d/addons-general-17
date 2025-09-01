# -*- coding: utf-8 -*-
# Part of Ynext. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
import random
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplier_password = fields.Char('Supplier Password')
    last_password_update = fields.Datetime('Last Password Update')
    active_login = fields.Boolean('Active Login', default=False)
    token = fields.Char('Token')
    last_token_update = fields.Datetime('Last Token Update')

    def generate_token(self):
        random_token = random.randint(1000000000, 20000000000)
        self.token = str(self.id) + "-" + str(random_token) + "-" + str(self.name[0])
        self.last_token_update = fields.Datetime.now()

    @api.onchange('supplier_password')
    def _onchange_supplier_password(self):
        self.last_password_update = fields.Datetime.now()


    def action_send_email(self):
        _logger.info('Sending email')

        # Validate if the email is set
        if not self.email:
            raise UserError(_('Please set the email address for this supplier'))

        body_mail = """
        <p>Dear %s,</p>
        <p>Your password to access the supplier is: %s</p>
        <p>Best regards,</p>
        <p>Admin</p>
        """ % (self.name, self.supplier_password)

        mail_values = {
            'email_from': self.env.user.email,
            'email_to': self.email,
            'subject': 'Portal Supplier',
            'body_html': body_mail,
        }

        mail_id = self.env['mail.mail'].create(mail_values)

        mail_id.send()

    def action_create_password(self):
        _logger.info('action_create_password')
        random_password = random.randint(100000, 200000)
        self.supplier_password = str(random_password)
        self.last_password_update = fields.Datetime.now()