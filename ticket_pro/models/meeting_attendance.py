# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class MeetingAttendance(models.Model):
    _description = "Meeting Attendance"
    _name = 'meeting.attendance'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Many2one('directory.partner', string='Contacto')
    class_ticket_id = fields.Many2one('class.ticket', string='Clase')
    date = fields.Datetime('Fecha', default=fields.Datetime.now)