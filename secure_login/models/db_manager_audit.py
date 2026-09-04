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

"""Rastrea los intentos (exitosos y fallidos) de descargar (backup) o
eliminar una base de datos desde el Gestor de Bases de Datos
(``/web/database/manager``).

Esas rutas se resuelven fuera del registro de cualquier base de datos
concreta, así que la única forma de interceptarlas es "parchando" en
caliente ``odoo.service.db.check_super``, punto único por el que pasan
todas las operaciones protegidas por la contraseña maestra.
"""

import logging

from odoo import api, fields, models, SUPERUSER_ID
from odoo import registry as registry_get
from odoo.exceptions import AccessDenied
from odoo.http import request
from odoo.service import db as db_service

_logger = logging.getLogger(__name__)

_DB_ACTION_BY_PATH = {
    '/web/database/backup': 'backup',
    '/web/database/drop': 'drop',
}


class SecureDatabaseAction(models.Model):
    _name = 'secure.database.action'
    _description = 'Intentos de Descarga o Eliminación de Base de Datos'
    _order = 'date desc'

    date = fields.Datetime(string='Fecha y Hora', readonly=True)
    action = fields.Selection([
        ('backup', 'Descarga (Backup)'),
        ('drop', 'Eliminación'),
    ], string='Acción', readonly=True)
    database_name = fields.Char(string='Base de Datos', readonly=True)
    success = fields.Boolean(string='Exitoso', readonly=True)
    ip_address = fields.Char(string='Dirección IP', readonly=True)


def _pending_db_manager_action():
    """Si la petición HTTP en curso es un backup o drop desde el gestor
    de bases de datos, retorna (accion, nombre_bd, ip); si no, None."""
    if not request or not getattr(request, 'httprequest', None):
        return None
    action = _DB_ACTION_BY_PATH.get(request.httprequest.path)
    if not action:
        return None
    db_name = request.httprequest.form.get('name')
    if not db_name:
        return None
    ip = request.httprequest.environ.get('REMOTE_ADDR')
    return action, db_name, ip


def _register_db_manager_attempt(action, database_name, success, ip_address):
    """Escribe el intento en la propia base de datos objetivo (si existe
    y tiene este módulo instalado). Para un 'drop' exitoso esto ocurre
    antes de que la base sea eliminada, ya que la contraseña maestra se
    valida antes de ejecutar la operación."""
    try:
        with registry_get(database_name).cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            env['secure.database.action'].create({
                'date': fields.Datetime.now(),
                'action': action,
                'database_name': database_name,
                'success': success,
                'ip_address': ip_address,
            })
    except Exception as e:
        _logger.info(
            'secure_login: no se pudo registrar intento de %s sobre "%s": %s',
            action, database_name, e,
        )


_original_check_super = db_service.check_super


def _check_super_with_audit(passwd):
    try:
        result = _original_check_super(passwd)
    except AccessDenied:
        info = _pending_db_manager_action()
        if info:
            action, db_name, ip = info
            _register_db_manager_attempt(action, db_name, False, ip)
        raise
    info = _pending_db_manager_action()
    if info:
        action, db_name, ip = info
        _register_db_manager_attempt(action, db_name, True, ip)
    return result


_check_super_with_audit._secure_login_patched = True

if not getattr(db_service.check_super, '_secure_login_patched', False):
    db_service.check_super = _check_super_with_audit
