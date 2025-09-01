{
    "name": "purchase invoice valuation required",
    "version": "1.0",
    "summary": "Set Valuation attachment as mandatory in purchase invoice",
    "sequence": 10,
    "description": """
    Set Valuation attachment as mandatory in purchase invoice
    """,
    "website": "https://www.marlonfalcon.com",
    "depends": ["account", "purchase"],
    "category": "Purchase",
    "auto_install": False,
    "data": [
        "views/account_move_view.xml",
    ],
    "license": "LGPL-3",
}
