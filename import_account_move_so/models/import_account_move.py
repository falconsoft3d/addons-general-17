# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
import base64
import xlrd
from datetime import datetime, timedelta
import xlrd

class ImportAccountMove(models.Model):
    _description = "Import Account Move"
    _name = 'import.account.move'

    name = fields.Char('Description', copy=False, required=True)
    steep = fields.Integer('Steep', default=1, copy=True)
    position = fields.Integer('Position', default=1, copy=True)
    file = fields.Binary(string='File', required=True)
    file_name = fields.Char(string='File Name', required=True)
    active = fields.Boolean('Active', default=True)
    type = fields.Selection([
        ('1000', '1000'),
    ], string='Type', required=True, default='1000')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    journal_id = fields.Many2one('account.journal', string='Journal', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('charging', 'Charging'),
        ('done', 'Done'),
        ('error', 'Error'),
    ], string='State', required=True, default='draft')


    def cron_run_lot_account_import(self):
        _logger.info('cron_run_lot_account_import')
        lot_account_import = self.env['lot.account.import'].search([('active', '=', True)])
        for lot in lot_account_import:
            lot.action_import()


    def excel_to_date(self, excel_date):
        try:
            excel_base_date = datetime(1899, 12, 30)
            va = excel_base_date + timedelta(days=excel_date)
        except:
            # Today
            va = datetime.now()
        return va

    def action_import(self):
        self.ensure_one()
        _logger.info('action_import')

        if self.state == 'draft':
            self.state = 'charging'


        if self.state == 'charging':
            data = base64.b64decode(self.file)
            work_book = xlrd.open_workbook(file_contents=data)
            sheet = work_book.sheet_by_index(0)
            first_row = []

            for col in range(sheet.ncols):
                first_row.append(sheet.cell_value(0, col))

            cont = 0
            position = self.position
            to = self.steep + position
            self.position = to
            old_asiento = ''
            to_end = False
            account_move_arr = []

            if self.type == '1000':
                for count, row in enumerate(range(1, sheet.nrows), 2):
                    if row >= position and row <= to:
                        # row >= position and row <= to:
                        _logger.info('%s ----------------------------' % row)
                        record = {}
                        for col in range(sheet.ncols):
                            record[first_row[col]] = sheet.cell_value(row, col)

                        date = record['Fecha']
                        date = self.excel_to_date(date)
                        asiento = str(record['Asiento']).replace('.0', '')
                        cuenta = str(record['Cuenta']).replace('.0', '')
                        desc = record['Descripción']
                        cencep = record['Concepto']
                        debe = record['Debe']
                        haber = record['Haber']

                        _logger.info('->: %s, %s, %s, %s, %s, %s, %s,' % (date, asiento, cuenta, desc, cencep, debe, haber))

                        # Reviso si es un asiento nuevo
                        if asiento != old_asiento:
                            # Reviso si ese asiento ya existe
                            asiento_exist = self.env['account.move'].search([('name', '=', asiento)])
                            if asiento_exist:
                                _logger.info('Asiento ya existe: %s' % asiento)
                                old_asiento = asiento
                                account_move_arr.append(asiento)
                            else:
                                # Creo el asiento
                                asiento_id = self.env['account.move'].create({
                                    'date': date,
                                    'name': asiento,
                                    'ref': cencep,
                                    'journal_id': self.journal_id.id,
                                    'company_id': self.company_id.id,
                                    'old_id' : row,
                                    'import_account_move_id': self.id,
                                })
                                old_asiento = asiento
                                _logger.info('Asiento creado: %s' % asiento)
                                account_move_arr.append(asiento)
                        old_asiento = asiento

                # Creo la lineas
                _logger.info('account_move_arr: %s' % account_move_arr)



                for account_move in account_move_arr:
                    arr_lines = []
                    account_move_id = self.env['account.move'].search([('name', '=', account_move)])
                    _logger.info('account_move_id: %s' % account_move_id)
                    if account_move_id:
                        for count, row in enumerate(range(1, sheet.nrows), 2):
                            if row >= position and row <= to:
                                record = {}
                                for col in range(sheet.ncols):
                                    record[first_row[col]] = sheet.cell_value(row, col)
                                date = record['Fecha']
                                date = self.excel_to_date(date)
                                asiento = str(record['Asiento']).replace('.0', '')
                                cuenta = str(record['Cuenta']).replace('.0', '')
                                desc = record['Descripción']
                                cencep = record['Concepto']
                                debe = record['Debe'] if record['Debe'] else 0
                                haber = record['Haber'] if record['Haber'] else 0

                                _logger.info('->: debe %s, haber %s' % (debe, haber))


                                account_id = self.env['account.account'].search([
                                    ('code', '=', cuenta),
                                    ('company_id', '=', self.company_id.id)
                                ], limit=1)

                                if not account_id and cuenta != '':
                                    raise ValidationError(_('Account %s not found') % cuenta)


                                _logger.info('account_id: %s' % account_id)

                                vals_line = {
                                            'name': desc,
                                            'account_id': account_id.id,
                                            'debit': debe if debe > 0 else 0,
                                            'credit': haber if haber > 0 else 0,
                                            'date': date,
                                        }

                                _logger.info('vals_line: %s' % vals_line)

                                if asiento == account_move:
                                    arr_lines.append((0, 0, vals_line))

                    _logger.info('arr_lines: %s' % arr_lines)

                    # Insertamos sus lineas
                    if account_move_id.state == 'draft':
                        account_move_id.write({
                            'line_ids': arr_lines
                        })

                    # Confirmamos el asiento si esta en borrador
                    if account_move_id.state == 'draft':
                        account_move_id.action_post()

                    _logger.info('END')