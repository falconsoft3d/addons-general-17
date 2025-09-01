from odoo import models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        _logger.info('button_validate')
        for picking in self:
            if picking.supplier_reference:
                # Verifica si ya existe otro registro con el mismo name
                duplicate_picking = self.search([
                    ('supplier_reference', '=', picking.supplier_reference),
                    ('id', '!=', picking.id)  # Excluye el propio registro
                ], limit=1)

                _logger.info('duplicate_picking: %s' % duplicate_picking)

                if duplicate_picking:
                    raise ValidationError('El campo "Referencia" debe ser único. Ya existe otro registro con el mismo valor: %s' % duplicate_picking.name)

            else:
                _logger.info('No supplier_reference')
        # Llama al método original para continuar con la validación si no hay errores
        return super(StockPicking, self).button_validate()
