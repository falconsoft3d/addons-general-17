from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HomologationProcess(models.Model):
    _name = 'homologation.process'
    _description = 'Homologation Process'
    _inherit = ['mail.thread']  # si quieres chatter/tracking

    name = fields.Char(string='Name', copy=False, readonly=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    validation_date = fields.Date(string='Validation Date')
    approval_manager_id = fields.Many2one('res.users', string='Approval Manager')
    partner_approval_id = fields.Many2one('res.partner', string='Partner to Approve')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archive', 'Archive'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True)
    template_loaded = fields.Boolean(string='Template Loaded', default=False)
    notes = fields.Text()

    homologation_template_id = fields.Many2one(
        'homologation.template',
        string='Homologation Template'
    )

    line_data_ids = fields.One2many(
        'homologation.process.line',
        'process_id',
        string='Required Data'
    )
    line_document_ids = fields.One2many(
        'homologation.process.document',
        'process_id',
        string='Required Documents'
    )

    @api.model
    def create(self, vals):
        # Asignar secuencia al name
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('homologation.process.seq')
            vals['name'] = seq or _('New')
        return super(HomologationProcess, self).create(vals)

    def action_load_template_fields(self):
        self.ensure_one()
        if self.homologation_template_id:
            # Limpiar las referencias
            self.line_data_ids = [(5, 0, 0)]
            self.line_document_ids = [(5, 0, 0)]

            # Crea listas separadas (¡importante!)
            lines_data = []
            lines_document = []

            for template_line in self.homologation_template_id.line_ids:
                dict_vals = {
                    'template_line_id': template_line.id,
                    'name': template_line.name,
                    'field_type': template_line.field_type,
                    'required': template_line.required,
                    'category': template_line.category,
                }
                if template_line.category == 'data':
                    lines_data.append((0, 0, dict_vals))
                if template_line.category == 'document':
                    lines_document.append((0, 0, dict_vals))

            self.line_data_ids = lines_data
            self.line_document_ids = lines_document
            self.template_loaded = True

    def action_reload_template(self):
        if self.state == 'draft':
            self.ensure_one()
            self.line_data_ids = [(5, 0, 0)]
            self.line_document_ids = [(5, 0, 0)]
            self.template_loaded = False

    def action_validate_process(self):
        """Validar las lineas de homologacion antes de pasar a estado 'active'"""
        if not self.template_loaded:
            raise ValidationError(_('Template is required'))
        for line in self.line_data_ids:
            if line.required and not line.value_char and not line.value_number:
                raise ValidationError(_('Field %s is required') % line.name)

        for line in self.line_document_ids:
            if line.required and not line.value_binary:
                raise ValidationError(_('Document %s is required') % line.name)

        self.state = 'active'
        self.approval_manager_id = self.env.user.id
        self.partner_approval_id.homologation_state = "active"
        self.validation_date = fields.Date.today()
        # setear el tag en el partner
        tag_category = self.env["res.partner.category"].search([("name", "=", "Homologado")], limit=1)
        if tag_category not in self.partner_approval_id.category_id:
            self.partner_approval_id.category_id = [(4, tag_category.id)]

    def action_reject_process(self):
        self.state = 'rejected'

    def action_draft(self):
        self.state = 'draft'


class HomologationProcessLine(models.Model):
    _name = 'homologation.process.line'
    _description = 'Homologation Process Line'

    name = fields.Char(string='Field Name')
    field_type = fields.Selection([
        ('char', 'Texto / Char'),
        ('number', 'Numérico'),
    ], string='Type')
    required = fields.Boolean(string='Required')
    category = fields.Selection([
        ('data', 'Datos'),
    ], string='Category')
    # Valuees “reales” que se llenan
    value_char = fields.Char(string='Value Text')
    value_number = fields.Float(string='Value Number')

    # Relación al template_line original (para referencia)
    template_line_id = fields.Many2one(
        'homologation.template.line',
        string='Template Line',
    )
    # Relación al proceso
    process_id = fields.Many2one(
        'homologation.process',
        string='Homologation Process',
    )

    @api.constrains('value_char', 'value_number')
    def _check_values(self):
        for line in self:
            if line.required:
                if not line.value_char and not line.value_number:
                    raise ValidationError(_('Field %s is required') % line.name)    


class HomologationProcessDocument(models.Model):
    _name = 'homologation.process.document'
    _description = 'Homologation Process Document'

    name = fields.Char(string='Field Name')
    required = fields.Boolean(string='Required')
    field_type = fields.Selection([
        ('binary', 'Binary'),
    ], string='Type')
    category = fields.Selection([
        ('document', 'Document'),
    ], string='Category')
    value_binary = fields.Binary(string='Value Document')
    filename_binary = fields.Char(string='File name')  # Nombre del adjunto

    # Relación al template_line original (para referencia)
    template_line_id = fields.Many2one(
        'homologation.template.line',
        string='Template Line',
    )
    # Relación al proceso
    process_id = fields.Many2one(
        'homologation.process',
        string='Homologation Process',
    )

    @api.constrains('value_binary')
    def _check_values(self):
        for line in self:
            if line.required and not line.value_binary:
                    raise ValidationError(_('Field %s is required') % line.name)