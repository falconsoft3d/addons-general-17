import jinja2

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo import models, fields, _

import logging
_logger = logging.getLogger(__name__)

loader = jinja2.PackageLoader('odoo.addons.supplier_portal', 'views')
env = jinja2.Environment(loader=loader, autoescape=True)


class LoginSupplierController(http.Controller):

    @http.route('/supplier_portal/', methods=['GET'], auth='none')
    def login_endpoint(self, **kwargs):
        _logger.info("=login_endpoint 1=")
        company = http.request.env['res.company'].sudo().search([], limit=1)
        return env.get_template('login.html').render({
            'csrf_token': http.request.csrf_token(),
            'company': company,
            'company_fhone': company.phone,
            'company_email': company.email,
            'company_logo': company.logo and 'data:image/png;base64,%s' % company.logo.decode()
        })

    @http.route('/supplier_portal/login/check', type='json', auth='public', cors='*')
    def login_check(self, **kwargs):
        _logger.info("= login_check =")
        email = kwargs.get('email')
        password = kwargs.get('password')
        partner_id = http.request.env['res.partner'].sudo().search([
                                    ('email', '=', email),
                                    ('supplier_password', '=', password),
                                    ('active_login', '=', True)
                                                               ], limit=1)

        if partner_id:
            _logger.info("A")
            if partner_id.password == password:
                _logger.info("B")
                request.session['my_current_url'] = kwargs.get('url')
                return {
                    'status': 'ok',
                    'partner_id': partner_id.id
                }
            else:
                _logger.info("C")
                return {
                    'status': 'error',
                    'error': 'Password is incorrect',
                    'user': 0
                }
        else:
            _logger.info("D")
            return {
                'status': 'error',
                'error': 'Password is incorrect',
                'user': 0
            }