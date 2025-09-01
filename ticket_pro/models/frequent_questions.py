# -*- coding: utf-8 -*-

from odoo import api, fields, models

class FrequentQuestion(models.Model):
    _description = "Frequent Question"
    _name = 'frequent.question'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Char('Código', default="Nuevo", copy=False)
    entry_date = fields.Datetime(
        'Fecha de Entrada', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string='Usuario',
                              default=lambda self: self.env.user)

    question = fields.Text('Pregunta')
    answer = fields.Text('Respuesta')


    @api.model
    def create(self, vals):
        if vals.get('name', "Nuevo") == "Nuevo":
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'frequent.question') or "Nuevo"
        faq = super(FrequentQuestion, self).create(vals)
        return faq