from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        for arg in domain:
            if isinstance(arg, (list, tuple)) and arg[0] in ["default_code", "name", "barcode"]:
                field_name, operator, value = arg
                words = value.split(' ') if value else []
                if words and len(words) > 1:
                    domain = domain.copy()
                    domain.remove(arg)
                    for word in words:
                        domain.append(('name', 'ilike', word))
                    break
        if self._context.get('search_default_categ_id'):
            domain = domain.copy()
            domain.append((('categ_id', 'child_of', self._context['search_default_categ_id'])))
        return super()._search(domain, offset, limit, order, access_rights_uid)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        names = name.split(' ') if name else False
        if names and len(names) > 1:
            products = self.search([('name', 'ilike', n) for n in names])
            if args:
                products = products.filtered_domain(args)
            return products[:limit].name_get()
        return super().name_search(name=name, args=args, operator=operator, limit=limit)

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        for arg in domain:
            if isinstance(arg, (list, tuple)) and arg[0] in ["default_code", "name", "barcode"]:
                field_name, operator, value = arg
                if isinstance(value, str):
                    words = value.split(' ')
                    if words and len(words) > 1:
                        domain = domain.copy()
                        domain.remove(arg)
                        for word in words:
                            domain.append(('name', 'ilike', word))
                        break
        if self._context.get('search_default_categ_id'):
            domain = domain.copy()
            domain.append(('categ_id', 'child_of', self._context['search_default_categ_id']))
        return super()._search(domain, offset, limit, order, access_rights_uid)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        if self._context.get('search_default_categ_id'):
            domain = domain.copy()
            domain.append((('categ_id', 'child_of', self._context['search_default_categ_id'])))
        return super()._search(domain, offset, limit, order, access_rights_uid)

    """
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):

        args = expression.normalize_domain(args)
        for arg in args:
            if isinstance(arg, (list, tuple)) and (arg[0] == "name"):
                index = args.index(arg)
                names = arg[2].split(' ') if arg[2] else False

                cont = 0
                if names and len(names) > 1:
                    for n in names:
                        cont += 1
                        if cont == 1:
                            args = (
                                    args[:index] + ["|", ("name", arg[1], n)] + args[index:]
                            )
                        else:
                            args = (
                                    args[:index] + ["&", ("name", arg[1], n)] + args[index:]
                            )

                        index += 1
                break

            elif isinstance(arg, (list, tuple)) and (arg[0] == "description_sale"):
                index = args.index(arg)
                description_sale = arg[2].split(' ') if arg[2] else False

                cont = 0
                if description_sale and len(description_sale) > 1:
                    for n in description_sale:
                        cont += 1
                        if cont == 1:
                            args = (
                                    args[:index] + ["|", ("description_sale", arg[1], n)] + args[index:]
                            )
                        else:
                            args = (
                                    args[:index] + ["&", ("description_sale", arg[1], n)] + args[index:]
                            )

                        index += 1
                break
        return super().search(
            args, offset=offset, limit=limit, order=order, count=count
        )
        """

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        names = name.split(' ') if name else False
        if names and len(names) > 1:
            products = self.search([('name', 'ilike', n) for n in names])
            if args:
                products = products.filtered_domain(args)
            return products[:limit].name_get()
        return super().name_search(name=name, args=args, operator=operator, limit=limit)





