from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    valuation_binary = fields.Binary(string="Valuación")

    def button_validate(self):
        if self.picking_type_id.code == 'incoming' and not self.guide_reference:
            raise ValidationError(_("The reference guide is mandatory in this type of picking."))
        return super(StockPicking, self).button_validate()
