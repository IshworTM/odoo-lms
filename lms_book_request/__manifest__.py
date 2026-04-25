{
    "name": "OpenShelf LMS Book Request",
    "summary": """
        Manages Books Requests for Library Management System
        """,
    "description": """
        An odoo module to manage Book Requests for Library Management System
    """,
    "author": "Ishwor Dulal",
    "website": "https://github.com/IshworTM/odoo-lms",
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "va_lms"],
    "data": [
        "security/ir.model.access.csv",
        "views/lms_book_request_views.xml",
    ],
    "installable": True,
    "application": True,
}
