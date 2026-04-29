{
    "name": "OpenShelf LMS Book Website",
    "summary": """
        Manages Book Website for LMS
        """,
    "description": """
        An odoo module to manages Book Website for the OpenShelf LMS
    """,
    "author": "Ishwor Dulal",
    "website": "https://github.com/IshworTM/odoo-lms",
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "web", "website", "lms_book", "lms_book_issue"],
    "data": [
        "security/ir.model.access.csv",
        "views/library_book_template.xml",
        "views/library_template.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "lms_website_book/static/src/**/*.scss",
            "lms_website_book/static/src/**/*.js",
        ],
    },
    "installable": True,
    "application": True,
}
