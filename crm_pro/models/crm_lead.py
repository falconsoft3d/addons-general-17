# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging
_loger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    date_contact = fields.Date(string='Date Contact', default=fields.Date.context_today)
    numer_days_contact = fields.Integer(string='Number of Days Contact', compute='_compute_numer_days_contact')

    @api.depends('date_contact')
    def _compute_numer_days_contact(self):
        for record in self:
            if record.date_contact:
                # Calculamos la diferencia de días entre la fecha de contacto y la fecha actual
                days = (fields.Date.context_today(self) - record.date_contact).days
                record.numer_days_contact = days
            else:
                record.numer_days_contact = 0

    """
    Este metodo se encarga de enviar correos a los clientes potenciales una ves que se cumple el tiempo de contacto
    """
    def cron_send_email(self):
        _loger.info('=== begin cron_send_email === ')
        crm_pro_info_ids = self.env['crm.pro.info'].search([
            ('send_email', '=', True),
            ('numer_days', '>', 0),
        ])
        _loger.info(crm_pro_info_ids)
        for info in crm_pro_info_ids:
            _loger.info('=== info === %s', info.name)
            # buscamos todos los lead de la fecha del info
            # tomo la fecha de hoy y le resto el numero de dias
            date_to_rest = fields.Date.context_today(self) - relativedelta(days=info.numer_days)

            _loger.info('=== date_to_rest === %s', date_to_rest)

            lead_ids = self.env['crm.lead'].search([
                ('date_contact', '=', date_to_rest),
            ])
            _loger.info('=== info.numer_days === %s', info.numer_days)
            _loger.info(lead_ids)

            if len(lead_ids) > 0:
                for lead in lead_ids:
                    if lead.stage_id.crm_pro_info_id.numer_days != info.numer_days:
                        # Enviar correo al cliente
                        email_from = lead.company_id.email
                        email_to = lead.partner_id.email
                        email_title = info.email_title
                        body_html = info.email_body

                        # Enviar correo al cliente sin planilla
                        email = lead.env['mail.mail'].create({
                            'subject': email_title,
                            'email_from': email_from,
                            'email_to': email_to,
                            'body_html': body_html,
                        })
                        email.send()

                        # actualizamos la etapa del lead
                        stage_id = lead.env['crm.stage'].search([
                            ('crm_pro_info_id', '=', info.id),
                        ], limit=1)

                        if stage_id:
                            lead.stage_id = stage_id.id

        _loger.info('=== end cron_send_email === ')