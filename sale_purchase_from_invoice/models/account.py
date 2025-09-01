from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_to_so = fields.Boolean('Crear venta desde factura', related='company_id.invoice_to_so')
    invoice_to_po = fields.Boolean('Crear compra desde factura', related='company_id.invoice_to_po')
    order_created = fields.Boolean('Pedido creado', readonly=True)
    sale_id = fields.Many2one('sale.order', 'Pedido de Venta', readonly=True)

    def generate_sale(self, action_to):
        sale_order_obj = self.env['sale.order']
        for invoice in self:
            sale_lines = []
            for line in invoice.invoice_line_ids:
                if line.product_id and line.product_id.type != 'consu':
                    sale_lines.append((0, 0, {
                        'company_id':  line.company_id.id,
                        'currency_id': line.currency_id.id,
                        'product_uom': line.product_uom_id.id,
                        'product_id': line.product_id.id,
                        'invoice_lines': [(6, 0, [line.id])],
                        'name': line.name,
                        'price_unit': line.price_unit,
                        'discount': line.discount,
                        'product_uom_qty': line.quantity,
                        'tax_id': [(6, 0, line.tax_ids.ids)],
                    }))
            order = sale_order_obj.create({
                'partner_id': invoice.partner_id.id,
                'currency_id': invoice.currency_id.id,
                'company_id': invoice.company_id.id,
                'origin': invoice.name,
                'order_line': sale_lines,
                'invoice_ids': [(6, 0, [invoice.id])]
            })
            invoice.order_created = True
            invoice.sale_id = order.id
            if action_to == 'order_and_picking':
                order.action_confirm()

    def generate_purchase(self, action_to):
        purchase_order_obj = self.env['purchase.order']
        for invoice in self:
            purchase = purchase_order_obj.create({
                'partner_id': invoice.partner_id.id,
                'currency_id': invoice.currency_id.id,
                'company_id': invoice.company_id.id,
                'date_order': invoice.invoice_date,
            })

            purchase_lines = []
            for line in invoice.invoice_line_ids:
                if line.product_id:# and line.product_id.type != 'consu'
                    purchase_lines.append((0, 0, {
                        'company_id':  line.company_id.id,
                        'currency_id': line.currency_id.id,
                        'product_uom': line.product_uom_id and line.product_uom_id.id or line.product_id.uom_po_id.id,
                        'product_id': line.product_id.id,
                        'date_planned': invoice.invoice_date,
                        'invoice_lines': [(6, 0, [line.id])],
                        'name': line.name,
                        'price_unit': line.price_unit,
                        'product_qty': line.quantity,
                        'taxes_id': [(6, 0, line.tax_ids.ids)],
                    }))
            purchase.order_line = purchase_lines
            purchase.invoice_ids =  [(6, 0, [invoice.id])]

            invoice.order_created = True
            invoice.purchase_id = purchase.id
            if action_to == 'order_and_picking':
                purchase.button_confirm()
