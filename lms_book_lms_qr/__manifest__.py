{
    "name": "OpenShelf LMS QR",
    "summary": """
        Manages QR and books relationship
        """,
    "description": """
        An Odoo module to manages QR and books relationship
    """,
    "author": "Ishwor Dulal",
    "website": "https://github.com/IshworTM/odoo-lms",
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["lms_book", "lms_qr_generator"],
    "data": [
        "views/lms_book_views.xml",
    ],
    "auto_install": True,
}
