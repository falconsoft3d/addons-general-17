from datetime import datetime

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_homologated = fields.Boolean(
        string="Homologado",
        default=False,
        compute="_compute_is_homologated",
        store=True,
    )
    homologation_state = fields.Selection(
        string="Estado de homologación",
        selection=[
            ("draft", "Draft"),
            ("requested", "requested"),
            ("active", "Active"),
            ("inactive", "Inactive"),
        ],
        default="inactive",
        tracking=True,
        store=True,
        compute="_compute_homologation_state",
    )

    contrat_homologation = fields.Binary(string="Contrato de homologación")
    etica_homologation = fields.Binary(string="Video de ética")

    @api.depends('homologation_state')
    def _compute_is_homologated(self):
        for rec in self:
            if rec.homologation_state == "active":
                rec.is_homologated = True

    homologation_process_id = fields.Many2one(
        comodel_name="homologation.process",
        string="Active Process",
        compute="_compute_active_process",
        required=False,
    )
    homologation_process_ids = fields.One2many(
        "homologation.process", "partner_approval_id", string="Process", required=False
    )
    homologation_date = fields.Date(
        string="Last Date Homologation",
        related="homologation_process_id.validation_date",
        tracking=True,
    )
    request_homologation = fields.Boolean(
        string='Request homologation',
        required=False)

    allow_po_no_check  = fields.Boolean(
        string='Allow confirm PO without homologation',
        default=True)

    @api.depends("homologation_process_ids")
    def _compute_active_process(self):
        for rec in self:
            rec.homologation_process_id = False
            if rec.homologation_process_ids:
                active_process = self.env["homologation.process"].search(
                    [("partner_approval_id", "=", rec.id), ("state", "=", "active")],
                    limit=1,
                )
                rec.homologation_process_id = active_process if active_process else False
                if not active_process:
                    draft_process = rec.homologation_process_id = self.env["homologation.process"].search(
                        [("partner_approval_id", "=", rec.id), ("state", "=", "draft")],
                        limit=1,
                    )
                    rec.homologation_process_id = draft_process if draft_process else False

    line_data_ids = fields.One2many(
        related="homologation_process_id.line_data_ids", string="Required Data"
    )
    line_document_ids = fields.One2many(
        related="homologation_process_id.line_document_ids", string="Required Documents"
    )

    @api.depends("homologation_process_id")
    def _compute_homologation_state(self):
        tag_category = self.env["res.partner.category"].search([("name", "=", "Homologado")], limit=1)

        for rec in self:
            rec.homologation_state = "inactive"
            rec.is_homologated = False
            if tag_category in rec.category_id:
                rec.category_id = [(3, tag_category.id)]

            if rec.homologation_process_id:
                if rec.homologation_process_id.state == "active":
                    rec.homologation_state = "active"
                    rec.is_homologated = True
                    # Agregamos la categoría con la tupla (4, id)
                    if tag_category not in rec.category_id:
                        rec.category_id = [(4, tag_category.id)]


    def action_view_homologation(self):
        """ Acción para ver los procesos de homologación asociados al partner en estado draft"""
        self.ensure_one()
        action = self.env.ref("provider_homologation.action_homologation_process").read()[0]
        action["domain"] = [
            ("partner_approval_id", "=", 'draft'),
            ("state", "=", self.id),
        ]
        return action

    def create_request_homologation(self):
        """ Crea un nuevo proceso de homologación asociado al partner en estado draft"""
        self.ensure_one()
        self.env["homologation.process"].create(
            {
                "partner_approval_id": self.id,
                "state": "draft",
            }
        )

    def action_request_homologation(self):
        for rec in self:
            rec.create_request_homologation()
            rec.homologation_state = "requested"
            rec.request_homologation = True

            # Referenciamos la plantilla de correo
            template = self.env.ref(
                "provider_homologation.email_template_homologation_request"
            )
            if not template:
                continue

            # Preparamos los valores para enviar por mail_values (para forzar que se envíe a correos específicos)
            mail_values = {}
            recipient_list = []

            # 1) Agregamos el correo del partner (proveedor)
            if rec.email:
                recipient_list.append(rec.email)

            # 2) Obtenemos el Homologation Manager definido en Ajustes
            #    En Odoo 15+ get_values() retorna un diccionario con los config_parameters,
            #    incluida la clave "homologation_manager"
            config_values = self.env["res.config.settings"].sudo().get_values()
            manager_id = config_values.get("homologation_manager")

            # Validamos y obtenemos el email del Manager
            if manager_id:
                manager_user = self.env["res.users"].sudo().browse(manager_id)
                if manager_user and manager_user.email:
                    recipient_list.append(manager_user.email)

            # 3) Si hay destinatarios, construimos el email_to (puedes usar CC o BCC si prefieres)
            if recipient_list:
                mail_values["email_to"] = ",".join(recipient_list)

            # 4) Enviamos el correo usando la plantilla y forzando el envío
            template.sudo().send_mail(rec.id, email_values=mail_values, force_send=True)

    @api.model
    def _check_homologation_period(self):
        """Se ejecuta cada mes vía cron."""
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        current_month = datetime.now().month
        #first_m = IrConfigParameter.get_param("first_month_check", default=1)
        #second_m = IrConfigParameter.get_param("second_month_check", default=1)
        third_m = IrConfigParameter.get_param("third_month_check", default=1)
        if current_month == third_m:
            # Buscar proveedores homologados y verificar vigencia, etc.
            partners = self.search([("is_homologated", "=", True)])
            for partner in partners:
                # buscamos si tiene algun proceso active y lo ponemos a archive
                if partner.homologation_process_id:
                    partner.homologation_process_id.write({"state": "archive"})
