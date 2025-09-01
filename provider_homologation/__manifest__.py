{
    "name": "Provider Homologation MFH",
    "version": "1.2",
    "summary": "Approval Process for Providers",
    "sequence": 10,
    "description": """
================================
Allows users to configure an approval process for their providers.
    """,
    "category": "Purchase",
    "website": "https://www.marlonfalcon.com",
    "depends": [
        "contacts",
        "purchase",
        "mail",  # Para tracking y notificaciones
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/homologation_template_views.xml",
        "views/homologation_process_views.xml",
        "views/res_settings.xml",
        "views/menu_homologation.xml",
        "views/purchase_order_views.xml",
        "views/res_partner_views.xml",
        "data/data.xml",
        "data/category_data.xml",
        "data/mail_template_data.xml",
        "data/homologation_template_data.xml",
        "data/cron_data.xml",
    ],
    "auto_install": False,
    "license": "LGPL-3",
}
