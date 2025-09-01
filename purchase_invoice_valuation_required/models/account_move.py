from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    valuation_file = fields.Binary(string="Valuación Manual")
    invoice_file = fields.Binary(string="Factura Manual")

    def action_post(self):
        if self.move_type == 'in_invoice' and not self.valuation_file:
            raise ValidationError(_("La Valuación es obligatoria en este tipo de Factura."))

        if self.move_type == 'in_invoice' and not self.invoice_file:
            raise ValidationError(_("La Factura Manual es obligatoria en este tipo de Factura."))

        return super(AccountMove, self).action_post()
