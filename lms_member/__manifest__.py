{
    "name": "OpenShelf LMS Member",
    "summary": """
        Manages LMS members
        """,
    "description": """
        An odoo module to manage members for OpenShelf Library Management System
    """,
    "author": "Ishwor Dulal",
    "website": "https://github.com/IshworTM/odoo-lms",
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "mail", "va_lms"],
    "data": [
        "security/lms_member_security.xml",
        "security/ir.model.access.csv",
        "views/lms_member_views.xml",
    ],
    "installable": True,
    "application": True,
}
