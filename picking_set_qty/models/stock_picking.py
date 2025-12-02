from odoo import models, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_set_quantities_to_zero(self):
        """Establece todas las cantidades de las líneas de picking a 0"""
        for picking in self:
            # Establecer cantidad a 0 en todas las líneas
            for move in picking.move_ids_without_package:
                move.quantity = 0.0
            
            # Registrar mensaje en el chatter
            picking.message_post(
                body=_("Las cantidades de todas las líneas han sido establecidas a 0."),
                subject=_("Cantidades establecidas a 0"),
                message_type='notification',
            )
        
        return True
