# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_history_ids = fields.One2many(
        'product.price.history',
        'product_tmpl_id',
        string='Histórico de Precios'
    )
    
    price_history_count = fields.Integer(
        string='Cantidad de Cambios',
        compute='_compute_price_history_count'
    )

    @api.depends('price_history_ids')
    def _compute_price_history_count(self):
        for record in self:
            record.price_history_count = len(record.price_history_ids)

    def write(self, vals):
        """Sobrescribe write para registrar cambios en el histórico"""
        # Verificamos si se está cambiando el coste o el precio de venta
        if 'standard_price' in vals or 'list_price' in vals:
            for record in self:
                # Obtenemos los valores actuales antes del cambio
                old_standard_price = record.standard_price
                old_list_price = record.list_price
                
                # Obtenemos los nuevos valores (si no están en vals, mantenemos los antiguos)
                new_standard_price = vals.get('standard_price', old_standard_price)
                new_list_price = vals.get('list_price', old_list_price)
                
                # Solo registramos si hay un cambio real
                if new_standard_price != old_standard_price or new_list_price != old_list_price:
                    # Ejecutamos el write primero
                    res = super(ProductTemplate, record).write(vals)
                    
                    # Creamos el registro en el histórico
                    self.env['product.price.history'].create({
                        'product_tmpl_id': record.id,
                        'user_id': self.env.user.id,
                        'standard_price': new_standard_price,
                        'list_price': new_list_price,
                    })
                    return res
        
        return super(ProductTemplate, self).write(vals)
