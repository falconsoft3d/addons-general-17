{
    "name": "Picking Available Stock",
    "version": "17.0",
    "summary": "Allows users to see availability of products in a location before validating a stock.picking",
    "sequence": 10,
    "description": """
Father (TOTP)
================================
Allows users to see availability of products in a location before validating a stock.picking
    """,
    "category": "Inventory",
    "website": "https://www.marlonfalcon.com",
    "depends": [
        "base",
        "stock",
    ],
    "auto_install": False,
    "data": [
        "views/stock_picking_view.xml",
    ],
    "license": "LGPL-3",
}
