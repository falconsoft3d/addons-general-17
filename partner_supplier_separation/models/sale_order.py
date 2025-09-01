# -*- coding: utf-8 -*-

from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    domain_partner_id = fields.Many2many('res.partner')

    @api.onchange('partner_id')
    def onchange_partner_id_as_customer(self):
        customers = self.env['res.partner'].search([('customer','=',True)])
        domain = []
        for customer in customers:
            if not customer.company_id or customer.company_id == self.company_id:
                domain.append(customer.id)       
        self.domain_partner_id = domain
        

