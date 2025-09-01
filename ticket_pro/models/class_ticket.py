# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class ClassTicket(models.Model):
    _description = "Class Ticket"
    _name = 'class.ticket'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Char('Nombre')
    date = fields.Date('Fecha')
    type = fields.Selection([
        ('class', 'Clase'),
        ('meet', 'Reunión'),
    ], string='Tipo', default='class')
    attendance_plan = fields.Integer('Asistentes Planificados')

    meeting_attendance_ids = fields.One2many('meeting.attendance', 'class_ticket_id')
    meeting_attendance_count = fields.Integer(string='Total de Asistentes', compute='compute_meeting_attendance_count')

    def compute_meeting_attendance_count(self):
        for record in self:
            record.meeting_attendance_count = len(record.meeting_attendance_ids)

    # ticket_pro.meeting_attendance_act
    def view_meeting_attendance(self):
        action = self.env.ref('ticket_pro.meeting_attendance_action').read()[0]
        action['domain'] = [('class_ticket_id', '=', self.id)]
        action['context'] = {
                              'default_class_ticket_id': self.id,
                            }
        return action