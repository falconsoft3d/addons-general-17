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
import json
from odoo import models, fields, api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

# Campos de res.company que, al cambiar, generan un registro de auditoría
_COMPANY_TRACKED_FIELDS = {
    'name': u'Nombre',
    'street': u'Dirección',
    'street2': u'Dirección 2',
    'city': u'Ciudad',
    'zip': u'Código Postal',
    'phone': u'Teléfono',
    'email': u'Correo',
    'website': u'Sitio Web',
    'vat': u'RUT / NIF',
    'currency_id': u'Moneda',
    'country_id': u'País',
    'state_id': u'Estado/Región',
    'logo': u'Logo',
    'favicon': u'Favicon',
    'company_registry': u'Registro de la Empresa',
}


class SecureAuditLog(models.Model):
    _name = 'secure.audit.log'
    _description = u'Log de Seguridad'
    _order = 'date desc'

    # Tipos de evento disponibles
    EVENT_USER_CREATED = 'user_created'
    EVENT_COMPANY_CHANGED = 'company_changed'
    EVENT_CONFIG_CHANGED = 'config_changed'

    EVENT_TYPES = [
        ('user_created', u'Usuario creado'),
        ('company_changed', u'Configuración de compañía modificada'),
        ('config_changed', u'Parámetro de configuración modificado'),
    ]

    date = fields.Datetime(
        string=u'Fecha y Hora',
        readonly=True,
        default=fields.Datetime.now,
    )
    event_type = fields.Selection(
        EVENT_TYPES,
        string=u'Tipo de Evento',
        readonly=True,
        required=True,
    )
    operator_id = fields.Many2one(
        'res.users',
        string=u'Ejecutado por',
        readonly=True,
        ondelete='set null',
    )
    target_user_id = fields.Many2one(
        'res.users',
        string=u'Usuario afectado',
        readonly=True,
        ondelete='set null',
    )
    company_id = fields.Many2one(
        'res.company',
        string=u'Compañía',
        readonly=True,
        ondelete='set null',
    )
    description = fields.Text(
        string=u'Detalle',
        readonly=True,
    )

    @api.model
    def _log(self, event_type, description, target_user_id=None, company_id=None):
        """Método interno para registrar eventos de auditoría."""
        try:
            self.sudo().create({
                'event_type': event_type,
                'operator_id': self.env.uid,
                'date': fields.Datetime.now(),
                'description': description,
                'target_user_id': target_user_id,
                'company_id': company_id,
            })
        except Exception:
            _logger.exception('secure_audit_log: error al registrar evento %s', event_type)


class ResUsersAudit(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        user = super(ResUsersAudit, self).create(vals)
        login = vals.get('login', u'')
        name = vals.get('name', u'')
        description = u'Nuevo usuario creado.\nNombre: %s\nLogin: %s' % (name, login)
        self.env['secure.audit.log']._log(
            event_type=SecureAuditLog.EVENT_USER_CREATED,
            description=description,
            target_user_id=user.id,
        )
        return user


class ResCompanyAudit(models.Model):
    _inherit = 'res.company'

    def write(self, vals):
        # Capturar valores anteriores para campos rastreados
        tracked = {k: v for k, v in vals.items() if k in _COMPANY_TRACKED_FIELDS}
        if tracked:
            before = {}
            for company in self:
                before[company.id] = {}
                for field in tracked:
                    raw = company[field]
                    # Para Many2one guardar el nombre legible
                    if hasattr(raw, 'name'):
                        before[company.id][field] = raw.name or u''
                    elif raw is False or raw is None:
                        before[company.id][field] = u''
                    else:
                        before[company.id][field] = raw

        result = super(ResCompanyAudit, self).write(vals)

        if tracked:
            for company in self:
                lines = []
                for field, label in _COMPANY_TRACKED_FIELDS.items():
                    if field not in tracked:
                        continue
                    old_val = before[company.id].get(field, u'')
                    new_raw = company[field]
                    if hasattr(new_raw, 'name'):
                        new_val = new_raw.name or u''
                    elif new_raw is False or new_raw is None:
                        new_val = u''
                    else:
                        new_val = new_raw
                    if field in ('logo', 'favicon'):
                        # Son binarios — solo indicar si cambió
                        if bool(old_val) != bool(new_val):
                            lines.append(u'%s: [modificado]' % label)
                    else:
                        old_str = u'%s' % old_val
                        new_str = u'%s' % new_val
                        if old_str != new_str:
                            lines.append(
                                u'%s: "%s" → "%s"' % (label, old_str, new_str)
                            )
                if lines:
                    description = (
                        u'Compañía: %s\n' % (company.name or u'')
                        + u'\n'.join(lines)
                    )
                    self.env['secure.audit.log']._log(
                        event_type=SecureAuditLog.EVENT_COMPANY_CHANGED,
                        description=description,
                        company_id=company.id,
                    )

        return result


# Prefijos de ir.config_parameter sin interés de seguridad (muy frecuentes)
_CONFIG_IGNORED_PREFIXES = (
    'web.base.url',
    'base_setup.',
    'mail.catchall',
    'mail.bounce',
)


class IrConfigParameterAudit(models.Model):
    _inherit = 'ir.config_parameter'

    def write(self, vals):
        if 'value' in vals:
            old_values = {rec.id: (rec.key, rec.value) for rec in self}
        result = super().write(vals)
        if 'value' in vals:
            for rec in self:
                key, old_value = old_values[rec.id]
                new_value = rec.value
                if old_value == new_value:
                    continue
                if any(key.startswith(p) for p in _CONFIG_IGNORED_PREFIXES):
                    continue
                description = (
                    u'Parámetro: %s\nAnterior: %s\nNuevo: %s'
                    % (key, old_value, new_value)
                )
                try:
                    self.env['secure.audit.log']._log(
                        event_type=SecureAuditLog.EVENT_CONFIG_CHANGED,
                        description=description,
                    )
                except Exception:
                    _logger.exception(
                        'secure_audit_log: error al registrar cambio de parámetro %s', key
                    )
        return result

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        key = vals.get('key', '')
        value = vals.get('value', '')
        if key and not any(key.startswith(p) for p in _CONFIG_IGNORED_PREFIXES):
            description = u'Parámetro creado: %s\nValor: %s' % (key, value)
            try:
                self.env['secure.audit.log']._log(
                    event_type=SecureAuditLog.EVENT_CONFIG_CHANGED,
                    description=description,
                )
            except Exception:
                _logger.exception(
                    'secure_audit_log: error al registrar creación de parámetro %s', key
                )
        return rec
