#-*- coding: utf-8 -*-

from odoo import api, fields, models, _

from odoo.exceptions import UserError

class RunSqlWzd(models.TransientModel):
    _name = 'run.sql.wzd'
    _description = "SQL WSD"

    sql_query = fields.Text(required=True)

    def action_run_sql(self):
        self.env.cr.execute(self.sql_query)