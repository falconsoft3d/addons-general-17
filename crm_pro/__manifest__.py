{
    'name': 'CRM PRO MFH',
    'version' : '1.2',
    'summary': 'Invoices & Payments',
    'sequence': 10,
    'description': """
CRM-PRO
================================
Manejo de CRM para Odoo 17
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.marlonfalcon.com',
    'depends': ['base', 'crm'],
    'category': 'Extra Tools',
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'views/crm_pro_info_views.xml',
        'views/menu_views.xml',
        'views/crm_stage_views.xml',
        'views/crm_lead_views.xml',
        'data/ir_cron.xml',
        'data/ir_config_parameter.xml',
    ],
    'license': 'LGPL-3',
}