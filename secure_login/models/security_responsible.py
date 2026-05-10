# coding: utf-8
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2018 Marlon Falcón Hernandez
#    (<http://www.falconsolutions.cl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

# Umbral de alerta: N intentos fallidos en WINDOW_SECONDS segundos
ALERT_THRESHOLD = 10
ALERT_WINDOW_SECONDS = 60


class SecurityResponsible(models.Model):
    _name = 'security.responsible'
    _description = u'Responsables de Seguridad'
    _order = 'sequence, id'

    sequence = fields.Integer(string=u'Secuencia', default=10)
    partner_id = fields.Many2one(
        'res.partner',
        string=u'Responsable',
        required=True,
        ondelete='cascade',
    )
    email = fields.Char(
        string=u'Correo',
        related='partner_id.email',
        store=True,
        readonly=True,
    )
    active = fields.Boolean(string=u'Activo', default=True)
    notes = fields.Char(string=u'Notas')

    _sql_constraints = [
        ('partner_unique', 'unique(partner_id)',
         u'Este contacto ya está registrado como responsable de seguridad.'),
    ]

    @api.model
    def get_alert_emails(self):
        """Retorna lista de emails de responsables activos con email configurado."""
        responsibles = self.search([('active', '=', True), ('email', '!=', False)])
        return [r.email for r in responsibles if r.email]

    @api.model
    def send_brute_force_alert(self, failed_count, window_seconds, login, ip_address):
        """Envía alerta de fuerza bruta a todos los responsables activos."""
        emails = self.get_alert_emails()
        if not emails:
            _logger.warning(
                'security_responsible: alerta de fuerza bruta detectada pero '
                'no hay responsables con email configurado.'
            )
            return

        body_html = (
            u'<p>Se ha detectado un posible ataque de <strong>fuerza bruta</strong> '
            u'en el sistema.</p>'
            u'<table style="border-collapse:collapse;margin:12px 0;">'
            u'<tr><td style="padding:4px 12px 4px 0;"><strong>Login atacado:</strong></td>'
            u'<td style="padding:4px 0;">%s</td></tr>'
            u'<tr><td style="padding:4px 12px 4px 0;"><strong>IP de origen:</strong></td>'
            u'<td style="padding:4px 0;">%s</td></tr>'
            u'<tr><td style="padding:4px 12px 4px 0;"><strong>Intentos fallidos:</strong></td>'
            u'<td style="padding:4px 0;color:#c0392b;font-weight:bold;">%d en los últimos %d segundos</td></tr>'
            u'</table>'
            u'<p style="color:#888;font-size:12px;">'
            u'Revise los logs de seguridad en el sistema para más detalles.</p>'
        ) % (login or u'desconocido', ip_address or u'desconocida',
             failed_count, window_seconds)

        for email in emails:
            try:
                mail = self.env['mail.mail'].create({
                    'subject': u'[ALERTA] Posible ataque de fuerza bruta detectado',
                    'body_html': body_html,
                    'email_to': email,
                    'auto_delete': True,
                })
                mail.send()
                _logger.info(
                    'security_responsible: alerta de fuerza bruta enviada a %s', email
                )
            except Exception:
                _logger.exception(
                    'security_responsible: error al enviar alerta a %s', email
                )
