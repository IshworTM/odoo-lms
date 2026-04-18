{
    "name": "OpenShelf LMS Issue Book",
    "summary": """
        Manages LMS Issue of Book
        """,
    "description": """
        An odoo module to manage book issue Library Management System
    """,
    "author": "Ishwor Dulal",
    "website": "https://github.com/IshworTM/odoo-lms",
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "mail", "lms_book", "lms_member"],
    "data": [
        "security/lms_book_issue_security.xml",
        "security/ir.model.access.csv",
        "views/lms_book_issue_views.xml",
        "views/lms_book_inherit_views.xml",
        "views/lms_member_inherit_views.xml",
        "views/res_config_settings.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": True,
}
