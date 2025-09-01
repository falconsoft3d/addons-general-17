{
    "name": "picking_reference_required",
    "version": "1.0",
    "summary": "Set invoice reference attachment as mandatory in incoming stock selection",
    "sequence": 10,
    "description": """
    Set invoice reference attachment as mandatory in incoming stock selection
    """,
    "website": "https://www.marlonfalcon.com",
    "depends": ["stock"],
    "category": "Stock",
    "auto_install": False,
    "data": [
        "views/stock_picking_view.xml",
    ],
    "license": "LGPL-3",
}
