# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CourseTaken(models.Model):
    _description = "Course Taken"
    _name = 'course.taken'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    employee_courses_id = fields.Many2one('employee.courses', string='Course')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    date = fields.Date('Date')
    expiration_date = fields.Date('Expiration Date')
    state = fields.Selection([
        ('active', 'active'),
        ('expired', 'expired'),
    ], string='State', default='active', track_visibility='onchange')


    @api.onchange('date', 'expiration_date')
    def _onchange_dates(self):
        if self.date and self.expiration_date:
            if self.date > self.expiration_date:
                raise ValidationError(_('Expiration Date must be greater than Date'))

            if self.expiration_date < fields.Date.today():
                self.state = 'expired'
            else:
                self.state = 'active'

        return {'value': {}}