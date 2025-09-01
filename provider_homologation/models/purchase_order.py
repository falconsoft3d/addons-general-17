from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    has_homologation = fields.Boolean(
        string="Have Approval",
        default=False,
        readonly=True,
    )
    homologation_required = fields.Boolean(
        string="Require Homologation", compute="_compute_homologation"
    )

    def set_homologation(self):
        self.has_homologation = True

    @api.depends("partner_id", "amount_total")
    def _compute_homologation(self):
        param_obj = self.env["ir.config_parameter"]
        amount_limit = float(
            param_obj.sudo().get_param(
                "provider_homologation.amount_min_to_approval", "0"
            )
        )
        for order in self:
            order.homologation_required = False

            if (
                order.amount_total > amount_limit
                and not order.partner_id.is_homologated
                and not order.partner_id.allow_po_no_check
            ):
                order.homologation_required = True

    def button_confirm(self):
        """Al confirmar, validar que si el total > X y no está homologado -> error"""
        param_obj = self.env["ir.config_parameter"]
        amount_limit = float(
            param_obj.sudo().get_param(
                "provider_homologation.amount_min_to_approval", "0"
            )
        )
        for order in self:
            if (
                    order.amount_total > amount_limit
                    and not order.partner_id.is_homologated
                    and not order.partner_id.allow_po_no_check
            ):
                raise UserError(
                    _("The supplier must be homologated to confirm this order")
                )
            order.set_homologation()
        return super(PurchaseOrder, self).button_confirm()
