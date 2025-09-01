import jinja2
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo import models, fields, _
import werkzeug
import werkzeug.utils
import json
import base64
from datetime import date
import logging
_logger = logging.getLogger(__name__)
import requests

loader = jinja2.PackageLoader('odoo.addons.crm_pro', 'web')
env = jinja2.Environment(loader=loader, autoescape=True)

class CrmPro(http.Controller):

    @http.route('/', methods=['GET'],  cors='*', auth='public')
    def crm_pro_contact_form(self, **kwargs):
        user = kwargs.get('user_id')
        company_id = http.request.env['res.company'].sudo().search([
            ('active', '=', True),
        ], limit=1)
        """
        template_id = http.request.env['customer.question.template'].sudo().search([
            ('key', '=', kwargs.get('key')),
            ('active', '=', True),
        ], limit=1)
        """
        return env.get_template('contact.html').render({
                'csrf_token': http.request.csrf_token(),
                'company_id': company_id,
            })



    @http.route('/crm_pro/contact_save', type='json', auth='public', cors='*')
    def crm_pro_contact_save(self, **kwargs):
        ok = True

        my_current_url = request.session.get('my_current_url')
        name = kwargs.get('name')
        email = kwargs.get('email')
        phone = kwargs.get('phone')
        text = kwargs.get('text')

        ir_config_parameter_url_id = http.request.env['ir.config_parameter'].sudo().search([
            ('key', '=', 'crm.pro.url'),
        ], limit=1)

        ir_config_parameter_chat_id = http.request.env['ir.config_parameter'].sudo().search([
            ('key', '=', 'crm.pro.chat'),
        ], limit=1)



        if ir_config_parameter_url_id and ir_config_parameter_chat_id:
            url = ir_config_parameter_url_id.value
            chat = ir_config_parameter_chat_id.value


            _initia_test = ">> Nuevo contacto desde la web crm.bim30.com \n"
            _test = _initia_test + "\n" + name + "\n" + email + " \n" + phone + " \n" + text + " \n"

            payload = json.dumps({
              "text": _test,
              "chat_id": chat,
            })

            headers = {
              'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, data=payload)





        # creamos el contacto si no existe por su email
        partner_id = http.request.env['res.partner'].sudo().search([
            ('email', '=', email),
        ], limit=1)

        if not partner_id:
            vals = {
                'name': name,
                'email': email,
                'phone': phone,
            }
            partner_id = http.request.env['res.partner'].sudo().create(vals)

        # buscamos el estado
        stage_id = http.request.env['crm.stage'].sudo().search([
            ('default_stage', '=', True),
        ], limit=1)

        if not stage_id:
            stage_id = http.request.env['crm.stage'].sudo().search([], limit=1)

        if name and email and phone:
            vals = {
                'name': name,
                'email_from': email,
                'phone': phone,
                'description': text,
                'user_id': 2,
                'partner_id': partner_id.id,
                'stage_id': stage_id.id,
            }
            lead_id = http.request.env['crm.lead'].sudo().create(vals)


            # Enviar correo al cliente
            company_id = http.request.env['res.company'].sudo().search([
                    ('active', '=', True),
                ], limit=1)

            email_from = company_id.email
            email_to = email
            email_title = stage_id.crm_pro_info_id.email_title
            body_html = stage_id.crm_pro_info_id.email_body

            # Enviar correo al cliente sin planilla
            email = http.request.env['mail.mail'].sudo().create({
                'subject': email_title,
                'email_from': email_from,
                'email_to': email_to,
                'body_html': body_html,
            })

            email.sudo().send()

        if ok:
            return {
                'status': 'ok',
            }
        else:
            return {
                'status': 'error',
            }