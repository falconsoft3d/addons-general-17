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
from datetime import datetime, timedelta
from odoo import models, fields, api, SUPERUSER_ID
from odoo import registry as registry_get
from .security_responsible import ALERT_THRESHOLD, ALERT_WINDOW_SECONDS

_logger = logging.getLogger(__name__)


class SecureLogin(models.Model):
    _name = 'secure.login'
    _description = 'Historial de Inicios de Sesión'
    _order = 'date desc'

    user_id = fields.Many2one('res.users', string='Usuario', readonly=True, ondelete='set null')
    login = fields.Char(string='Correo / Login', readonly=True)
    date = fields.Datetime(string='Fecha y Hora', readonly=True)
    ip_address = fields.Char(string='Dirección IP', readonly=True)


class SecureLoginFailed(models.Model):
    _name = 'secure.login.failed'
    _description = 'Intentos Fallidos de Acceso'
    _order = 'date desc'

    login = fields.Char(string='Login Intentado', readonly=True)
    date = fields.Datetime(string='Fecha y Hora', readonly=True)
    ip_address = fields.Char(string='Dirección IP', readonly=True)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        from odoo.exceptions import AccessDenied as _AccessDenied
        from odoo.http import request as _request

        ip = False
        try:
            if _request:
                ip = _request.httprequest.environ.get('REMOTE_ADDR', False)
        except Exception:
            pass

        try:
            uid = super()._login(db, login, password, user_agent_env=user_agent_env)
        except _AccessDenied:
            try:
                with registry_get(db).cursor() as cr:
                    env = api.Environment(cr, SUPERUSER_ID, {})
                    env['secure.login.failed'].create({
                        'login': login,
                        'date': fields.Datetime.now(),
                        'ip_address': ip,
                    })
                    try:
                        window_start = (
                            datetime.utcnow() - timedelta(seconds=ALERT_WINDOW_SECONDS)
                        ).strftime('%Y-%m-%d %H:%M:%S')
                        failed_count = env['secure.login.failed'].search_count([
                            ('ip_address', '=', ip),
                            ('date', '>=', window_start),
                        ])
                        if failed_count >= ALERT_THRESHOLD:
                            env['security.responsible'].send_brute_force_alert(
                                failed_count=failed_count,
                                window_seconds=ALERT_WINDOW_SECONDS,
                                login=login,
                                ip_address=ip,
                            )
                    except Exception:
                        _logger.exception(
                            'secure_login: error al verificar umbral de fuerza bruta'
                        )
            except Exception:
                _logger.exception('secure_login: error al registrar intento fallido')
            raise

        try:
            with registry_get(db).cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                env['secure.login'].create({
                    'user_id': uid,
                    'login': login,
                    'date': fields.Datetime.now(),
                    'ip_address': ip,
                })
        except Exception:
            _logger.exception('secure_login: error al registrar inicio de sesión')

        return uid
