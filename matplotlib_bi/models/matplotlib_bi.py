# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
import base64
import io
from io import BytesIO

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except (ImportError, IOError):
    plt = False
    _logger.warning('Missing external dependency matplotlib.')

class MatplotlibBi(models.Model):
    _description = "Matplotlib Bi"
    _name = 'matplotlib.bi'
    _order = 'id desc'

    name = fields.Char('Name', required=True)
    code = fields.Text('Code')
    type_origin = fields.Selection([
        ('matplotlib', 'Matplotlib'),
    ], 'Type', default='matplotlib')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', 'User', default=lambda self: self.env.user)
    analysis_graph = fields.Binary(readonly=True)

    array_not_allowed = ['delete', 'drop', 'exec', 'execute', 'import', 'open', 'write']


    def exe_update(self):
        for rec in self:
            _logger.info('Matplotlib BI: %s', rec.name)
            try:
                # Check if the code contains any of the forbidden words
                for word in rec.array_not_allowed:
                    if word in rec.code:
                        raise ValidationError(_('The word %s is not allowed in the code') % word)
                exec(rec.code)
            except Exception as e:
                raise ValidationError(_('Error in the execution of the Matplotlib code: %s') % str(e))