# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _update_website_published(self):
        _logger.info('Actualizando website_published para el producto: %s', self.name)
        for record in self:
            # Invertir el valor de website_published
            record.website_published = not record.website_published

    def _action_update_website_published(self):
        for record in self:
            record._update_website_published()



