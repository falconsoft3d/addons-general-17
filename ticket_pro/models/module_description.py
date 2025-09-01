# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import csv
import requests

class ModuleDescription(models.Model):
    _description = "Module Description"
    _name = 'module.description'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = 'id desc'

    name = fields.Char('Código', default="Nuevo", copy=False)
    module_id = fields.Many2one('ir.module.module', string='Módulo', tracking=True)
    category_id = fields.Many2one('ticket.category', string='Categoría', tracking=True)
    description = fields.Text('Observación')

    @api.model
    def create(self, vals):
        if vals.get('name', "Nuevo") == "Nuevo":
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'module.description') or "Nuevo"
        if 'category_id' not in vals:
            vals['category_id'] = self.env.ref('ticket_pro.ticket_proc_01').id
        doc = super().create(vals)
        return doc

    @api.model
    def cron_module_description(self):
        modules_obj = self.env['ir.module.module'].search([('state', '=', "installed")])
        url_csv_description = "https://raw.githubusercontent.com/falconsoft3d/addons_mfh/14.0/addons.csv"
        if url_csv_description:
            try:
                response = requests.get(url_csv_description)
                if response.status_code == 200:
                    lines = response.content.decode('utf-8').splitlines()
                    reader = csv.reader(lines)
                    for row in reader:
                        module = modules_obj.filtered(lambda x: x.name == row[0])
                        if module:
                            description = row[2]
                            if description:
                                module_description = self.search([('module_id', '=', module.id)])
                                if not module_description:
                                    self.create({
                                        'module_id': module.id,
                                        'description': description,
                                    })
            except Exception as e:
                pass