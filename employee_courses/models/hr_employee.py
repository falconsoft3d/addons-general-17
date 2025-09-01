# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.tools import float_round

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    course_taken_ids = fields.One2many('course.taken', 'employee_id', string='Course Taken')
    course_taken_count = fields.Integer(compute='_compute_course_taken_count', string='Course Taken Count')

    @api.depends('course_taken_ids')
    def _compute_course_taken_count(self):
        for record in self:
            record.course_taken_count = len(record.course_taken_ids)


    def action_view_course_taken(self):
        action = self.env.ref('employee_courses.action_course_taken').sudo().read()[0]
        action['domain'] = [('employee_id', '=', self.id)]
        action['context'] = {
            'default_employee_id': self.id,
        }
        return action
