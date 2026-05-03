{
    "name": "OpenShelf LMS",
    "summary": """
        Library Management System
        """,
    "description": """
        An Odoo module for the OpenShelf Library Management System
    """,
    "author": "Ishwor Dulal",
    "website": "https://github.com/IshworTM/odoo-lms",
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/lms_security.xml",
        "views/views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "va_lms/static/src/js/*.js",
        ]
    },
    "installable": True,
    "application": True,
}
