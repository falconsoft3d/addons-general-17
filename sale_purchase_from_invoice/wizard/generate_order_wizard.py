from odoo import fields, models


class GenerateOrderWizard(models.TransientModel):
    _name = 'generate.order.wizard'
    _description = 'Asistente para generacion de pedidos desde factura'

    action_to_do = fields.Selection([('only_order', 'Generar sólo pedido'),
                                     ('order_and_picking', 'Generar pedido y guía de despacho')],
                                    'Acción', default='only_order', required=True)

    def generate_order(self):
        for wizard in self:
            invoice = self.env['account.move'].browse(self.env.context.get('active_id')).exists()
            if invoice.move_type == 'out_invoice':
                invoice.generate_sale(wizard.action_to_do)
            elif invoice.move_type == 'in_invoice':
                invoice.generate_purchase(wizard.action_to_do)
