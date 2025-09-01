from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    guide_reference = fields.Binary(string="Guide reference")

    def button_validate(self):
        if self.picking_type_id.code == 'incoming' and not self.guide_reference:
            raise ValidationError(_("The reference guide is mandatory in this type of picking."))
        return super(StockPicking, self).button_validate()
