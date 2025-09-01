from odoo import fields, models, api

MONTHS_YEAR = [
    ("1", "January"),
    ("2", "February"),
    ("3", "March"),
    ("4", "April"),
    ("5", "May"),
    ("6", "June"),
    ("7", "July"),
    ("8", "August"),
    ("9", "September"),
    ("10", "October"),
    ("11", "November"),
    ("12", "December"),
]


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    amount_min_to_approval = fields.Float(
        string="Amount min request approval",
        config_parameter="provider_homologation.amount_min_to_approval",
    )  # si en la OC el monto es mayor a amount_min_to_approval requiere homologacion
    homologation_manager = fields.Many2one(
        "res.users",
        string="Homologation Manager",
        config_parameter="provider_homologation.homologation_manager",
    )  # Encargado de realizar el proceso de Homologacion
    first_approval = fields.Many2one(
        "res.users",
        string="First Approval",
        config_parameter="provider_homologation.first_approval",
    )
    first_month_check = fields.Selection(
        string="First Month Check",
        selection=MONTHS_YEAR,
        required=False,
    )
    second_month_check = fields.Selection(
        string="Second Month Check",
        selection=MONTHS_YEAR,
        required=False,
    )
    third_month_check = fields.Selection(
        string="Third Month Check",
        selection=MONTHS_YEAR,
        required=False,
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        #update the selection fields
        res.update(
            first_month_check=params.get_param('provider_homologation.first_month_check', default='1'),
            second_month_check=params.get_param('provider_homologation.second_month_check', default='2'),
            third_month_check=params.get_param('provider_homologation.third_month_check', default='3'),
        )
        return res

    def set_values(self):
        super().set_values()
        IrConfigParameter = self.env['ir.config_parameter'].sudo()
        # set the selection fields
        IrConfigParameter.set_param("provider_homologation.first_month_check", self.first_month_check)
        IrConfigParameter.set_param("provider_homologation.second_month_check", self.second_month_check)
        IrConfigParameter.set_param("provider_homologation.third_month_check", self.third_month_check)



