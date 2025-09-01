# -*- coding: utf-8 -*-
import datetime

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        obj = self.env['account.close.accounting.entries']
        if 'scheduled_date' in vals and vals['scheduled_date']:
            _date = fields.Date.from_string(str(vals['scheduled_date']))
        else:
            _date = datetime.date.today()

        sql = [('name','<=',_date),
                             ('date_to','>=',_date),
                             ('lock_stock' ,'=', True),
                             ('company_id','=',self.env.company.id)]

        period = obj.search(sql, limit=1, order='id desc')

        if period:
            raise UserError(_("It is not possible to create stock picking in this period because it is blocked!"))
        return super().create(vals)


    # Save the account.move.date in a variable and compare it with the period
    @api.model
    def save(self):
        obj = self.env['account.close.accounting.entries']
        if self.date:
            scheduled_date = self.scheduled_date

            period = obj.search([('name','<=',scheduled_date),
                                 ('lock_stock','>=',scheduled_date),
                                 ('lock_stock' ,'=', True),
                                 ('company_id','=',self.env.company.id)], limit=1, order='id desc')
            if period:
                raise UserError(_("It is not possible to modify stock picking in this period because it is blocked!"))
        return super(AccountMove, self).save()