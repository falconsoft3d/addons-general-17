# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EmployeeCourses(models.Model):
    _description = "Employee Courses"
    _name = 'employee.courses'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner', string='Partner')
    teacher = fields.Many2one('res.partner', string='Teacher')
    date = fields.Date('Date')

    course_taken_ids = fields.One2many('course.taken', 'employee_courses_id', string='Course Taken')
    course_taken_count = fields.Integer(compute='_compute_course_taken_count', string='Course Taken Count')

    @api.depends('course_taken_ids')
    def _compute_course_taken_count(self):
        for record in self:
            record.course_taken_count = len(record.course_taken_ids)


    def action_view_course_taken(self):
        action = self.env.ref('employee_courses.action_course_taken').read()[0]
        action['domain'] = [('employee_courses_id', '=', self.id)]
        action['context'] = {
            'default_employee_courses_id': self.id,
        }
        return action
