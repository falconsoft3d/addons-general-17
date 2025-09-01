# -*- coding: utf-8 -*-
import datetime

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        obj = self.env['account.close.accounting.entries']
        if 'date' in vals and vals['date']:
            invoice_date = fields.Date.from_string(str(vals['date']))
        else:
            invoice_date = datetime.date.today()

        sql = [('name','<=',invoice_date),
                             ('date_to','>=',invoice_date),
                             ('lock_accounting' ,'=', True),
                             ('company_id','=',self.env.company.id)]

        period = obj.search(sql, limit=1, order='id desc')

        if period:
            raise UserError(_("It is not possible to create assets in this period because it is blocked!"))
        return super().create(vals)


    # Save the account.move.date in a variable and compare it with the period
    @api.model
    def save(self):
        obj = self.env['account.close.accounting.entries']
        if self.date:
            invoice_date = self.date

            period = obj.search([('name','<=',invoice_date),
                                 ('date_to','>=',invoice_date),
                                 ('lock_accounting' ,'=', True),
                                 ('company_id','=',self.env.company.id)], limit=1, order='id desc')
            if period:
                raise UserError(_("It is not possible to modify assets in this period because it is blocked!"))
        return super(AccountMove, self).save()


    # block button_draft
    @api.model
    def button_draft(self):
        obj = self.env['account.close.accounting.entries']
        sql = [('name','<=',self.date),
                             ('date_to','>=',self.date),
                             ('lock_accounting' ,'=', True),
                             ('company_id','=',self.env.company.id)]
        period = obj.search(sql, limit=1, order='id desc')
        if period:
            raise UserError(_("It is not possible to change assets in this period because it is blocked!"))
        return super(AccountMove, self).button_draft()

    # block button_cancel
    @api.model
    def button_cancel(self):
        obj = self.env['account.close.accounting.entries']
        sql = [('name','<=',self.date),
                             ('date_to','>=',self.date),
                             ('lock_accounting' ,'=', True),
                             ('company_id','=',self.env.company.id)]
        period = obj.search(sql, limit=1, order='id desc')
        if period:
            raise UserError(_("It is not possible to change assets in this period because it is blocked!"))
        return super(AccountMove, self).button_cancel()

    # action_post
    @api.model
    def action_post(self):
        obj = self.env['account.close.accounting.entries']
        sql = [('name','<=',self.date),
                             ('date_to','>=',self.date),
                             ('lock_accounting' ,'=', True),
                             ('company_id','=',self.env.company.id)]
        period = obj.search(sql, limit=1, order='id desc')
        if period:
            raise UserError(_("It is not possible to change assets in this period because it is blocked!"))
        return super(AccountMove, self).action_post()




