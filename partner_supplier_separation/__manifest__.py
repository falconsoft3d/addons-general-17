##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2018 Marlon Falcon Hernandez
#    (<http://www.marlonfalcon.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Partner Supplier Separation MFH',
    'version': '17.0',
    'author': 'Marlon Falcon Hernandez',
    'maintainer': 'Marlon Falcon Hernandez',
    'website': 'http://www.marlonfalcon.com',
    'license': 'AGPL-3',
    'category': 'Extra Tools',
    'summary': 'Partner Supplier Separation.',
    'depends': ['base', 'sale_management', 'account','sale_management','purchase'],
    'price': 199.00,
    'currency': 'EUR',
    'data': [
        'views/res_partner_views.xml',
        'views/sale_order_inherit_view.xml',
        'views/purchase_order_inherit_view.xml',
        'views/product_supplier_info_inherit_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'post_init_hook': 'mark_contacts_as_customer_and_supplier',
}
