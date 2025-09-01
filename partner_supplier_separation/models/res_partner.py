# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def default_customer_rank(self):
        if self.customer_rank > 0:
            return True
        else:
            return False

    def default_supplier_rank(self):
        if self.supplier_rank > 0:
            return True
        else:
            return False

    creditor = fields.Boolean('Es Acreedor', copy=False)
    supplier = fields.Boolean('Es Proveedor', default=default_supplier_rank, copy=False)
    customer = fields.Boolean('Es Cliente', default=default_customer_rank, copy=False)

    @api.onchange('customer_rank')
    def onchange_customer_rank(self):
        if self.customer_rank > 0:
            self.customer = True
        else:
            self.customer = False

    @api.onchange('supplier_rank')
    def onchange_supplier_rank(self):
        if self.supplier_rank > 0:
            self.supplier = True
        else:
            self.supplier = False

    @api.onchange('customer')
    def onchange_customer(self):
        if self.customer == True:
            self.customer_rank = 1
        else:
            self.customer_rank = 0

    """
    @api.constrains('customer')
    def check_customer_commercial(self):
        if self.customer and not self.user_id:
            raise UserError("Debe definir comercial para este Cliente")"""

    @api.onchange('supplier')
    def onchange_supplier(self):
        if self.supplier == True:
            self.supplier_rank = 1
        else:
            self.supplier_rank = 0

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if res.customer:
            res.customer_rank = 1
        if res.supplier:
            res.supplier_rank = 1
        return res

    @api.model
    def function_partner_ranks(self):
        partners = self.env['res.partner'].search([])
        for partner in partners:
            if partner.customer_rank > 0:
                partner.customer = True
            if partner.supplier_rank > 0:
                partner.supplier = True


class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    domain_partner_id = fields.Many2many('res.partner')

    @api.onchange('partner_id')
    def onchange_name_domain(self):
        suppliers = self.env['res.partner'].search([('supplier', '=', True)])
        domain = []
        for sup in suppliers:
            domain.append(sup.id)
        self.domain_partner_id = domain
