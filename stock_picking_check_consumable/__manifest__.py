{
    "name": "Stock Auto Consume",
    "version": "1.2",
    "summary": "Check consumable option in product",
    "sequence": 10,
    "description": """
Check consumable option in product
    """,
    "category": "Inventory",
    "depends": ["stock", "purchase"],  # Dependemos del módulo stock
    "website": "https://www.marlonfalcon.com",
    "auto_install": False,
    "data": [
        "views/product_view.xml",
        "views/stock_picking_views.xml",
    ],
    "license": "LGPL-3",
}
