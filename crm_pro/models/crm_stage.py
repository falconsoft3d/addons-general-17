# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    crm_pro_info_id = fields.Many2one('crm.pro.info', string='Crm Information')
    default_stage = fields.Boolean(string='Default Stage', default=False)