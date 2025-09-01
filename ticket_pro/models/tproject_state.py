# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class TprojectState(models.Model):
    _description = "Tproject State"
    _name = 'tproject.state'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Char('Name', default="Etapa 01", copy=False)
    user_id = fields.Many2one('res.users', string='Creado',
                              default=lambda self: self.env.user)
    entry_date = fields.Datetime(
        'Fecha de Entrada', default=fields.Datetime.now)
    
    end_date = fields.Datetime(
        'Fecha de Finalizar')
    
    ticket_ids = fields.One2many('ticket.pro', 'tproject_state_id', 'Tickets')
    ticket_count = fields.Integer('N° Ticket', compute="_compute_ticket_count")
    ticket_not_end_count = fields.Integer('No resueltos', compute="_compute_ticket_not_end_count")
    
    @api.depends('ticket_ids')
    def _compute_ticket_count(self):
        for state in self:
            state.ticket_count = len(state.ticket_ids)
    
    @api.depends('ticket_ids')
    def _compute_ticket_not_end_count(self):
        count_end = 0
        for state in self:
            for ticket in state.ticket_ids:
                if ticket.state != "resuelto" or  ticket.state != "calificado" and ticket.tproject_state_id == state.id:
                    count_end += 1
            state.ticket_not_end_count = count_end
        
            
    def action_view_ticket(self):
        tickets = self.mapped('ticket_ids')
        action = self.env.ref('ticket_pro.action_ticket_pro').sudo().read()[0]
        action['domain'] = [('id', 'in', tickets.ids)]
        action['context'] = {'default_tproject_state_id': self.id}
        return action