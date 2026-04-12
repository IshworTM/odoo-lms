{
    "name": "OpenShelf LMS Books",
    "summary": """
        Manages Books for Library Management System
        """,
    "description": """
        An odoo module to manage books for Library Management System
    """,
    "author": "Ishwor Dulal",
    "website": "https://github.com/IshworTM/odoo-lms",
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "mail", "va_lms"],
    "data": [
        "security/lms_book_security.xml",
        "security/ir.model.access.csv",
        "views/lms_book_views.xml",
        "views/lms_book_author_views.xml",
        "views/lms_book_genre_views.xml",
    ],
    "installable": True,
    "application": True,
}
