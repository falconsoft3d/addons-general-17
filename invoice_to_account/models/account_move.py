# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging
import yaml
_logger = logging.getLogger(__name__)
try:
    from invoice2data.main import extract_data
    from invoice2data.extract.loader import read_templates
except ImportError:
    _logger.debug('Cannot `import invoice2data`.')
import tempfile
import os

class AccountMove(models.Model):
    _inherit = "account.move"

    file_name = fields.Char("File Name")
    file_data = fields.Binary(
        string='File',
        copy=False,
        help='Adjunto')

    converted = fields.Boolean(
        string='Converted',
        copy=False,
        default=False,
        help='Converted')

    # This method conver PDF to account.move and account.move.line in Odoo
    def read_invoice(self):
        template_content = self.partner_id.template_invoice
        if template_content:
            template = yaml.safe_load(template_content)

            print("template")
            print(template)

            # Write the binary data to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(self.file_data)
                tmp_file_path = tmp_file.name

            # Pass the temporary file path to extract_data
            res = extract_data(tmp_file_path, [template])
            print("res")
            print(res)

            # Delete the temporary file
            os.remove(tmp_file_path)
        else:
            _logger.error("No template found for partner")

    def cron_convert_invoice(self):
        print("cron_convert_invoice")
        invoices = self.env['account.move'].search([('converted', '=', False)], limit=100)
        for invoice in invoices:
            invoice.read_invoice()
