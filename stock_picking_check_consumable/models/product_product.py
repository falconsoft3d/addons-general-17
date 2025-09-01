from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    check_consume = fields.Boolean(string="Salida Automática Consumible")
