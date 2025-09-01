import jinja2

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo import models, fields, _

import logging
_logger = logging.getLogger(__name__)

loader = jinja2.PackageLoader('odoo.addons.supplier_portal', 'views')
env = jinja2.Environment(loader=loader, autoescape=True)


class LoginSupplierDashboardController(http.Controller):

    @http.route('/supplier_portal/home/<token>', methods=['GET'], auth='none')
    def home_endpoint(self, **kwargs):
        _logger.info("=home_endpoint=")

        token = kwargs.get('token')
        partner_id = http.request.env['res.partner'].sudo().search([('token', '=', token),
                                                                   ('active_login', '=', True)
                                                                   ], limit=1)


        company = http.request.env['res.company'].sudo().search([], limit=1)

        if not partner_id:
            return env.get_template('login.html').render({
                'csrf_token': http.request.csrf_token(),
                'company': company,
            })
        else:
            return env.get_template('home.html').render({
                'csrf_token': http.request.csrf_token(),
                'company': company,
                'company_fhone': company.phone,
                'company_email': company.email,
                'company_logo': company.logo and 'data:image/png;base64,%s' % company.logo.decode(),
                'virtual_user_id' : request.env.user,
            })