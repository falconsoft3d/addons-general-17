from odoo import models, fields

class HomologationTemplate(models.Model):
    _name = 'homologation.template'
    _description = 'Homologation Template'

    name = fields.Char(
        string='Template Name',
        required=True
    )
    line_ids = fields.One2many(
        'homologation.template.line',
        'template_id',
        string='Template Fields'
    )
    active = fields.Boolean(default=True)


class HomologationTemplateLine(models.Model):
    _name = 'homologation.template.line'
    _description = 'Homologation Template Line'

    name = fields.Char(string='Field Name', required=True)
    field_type = fields.Selection([
        ('char', 'Texto / Char'),
        ('number', 'Numérico'),
        ('binary', 'Documento (Binary)'),
    ], string='Type', required=True)

    required = fields.Boolean(string='Required', default=False)

    category = fields.Selection([
        ('data', 'Datos'),
        ('document', 'Documentos'),
    ], string='Category', required=True)

    template_id = fields.Many2one(
        'homologation.template',
        string='Template',
        ondelete='cascade'
    )

