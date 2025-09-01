from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_to_so = fields.Boolean('Crear venta desde factura')
    invoice_to_po = fields.Boolean('Crear compra desde factura')
