# -*- coding: utf-8 -*-

from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    domain_partner_id = fields.Many2many('res.partner')

    @api.onchange('partner_id')
    def onchange_partner_id_as_supplier_or_creditor(self):
        supplier_and_creditors = self.env['res.partner'].search(['|',('supplier','=',True),('creditor','=',True)])
        domain = []
        for partner in supplier_and_creditors:
            if not partner.company_id or partner.company_id == self.company_id:
                domain.append(partner.id)
        self.domain_partner_id = domain

