{
    "name": "OpenShelf LMS Qr Generator",
    "summary": """
        Manages QR for Library Management System
        """,
    "description": """
        An odoo module to manage QR for OpenShelf Library Management System
    """,
    "author": "Ishwor Dulal",
    "website": "https://github.com/IshworTM/odoo-lms",
    "category": "Uncategorized",
    "version": "0.1",
    "license": "LGPL-3",
    "depends": ["base", "mail", "va_lms"],
    "data": [
        "security/lms_qr_security.xml",
        "security/ir.model.access.csv",
        "views/lms_qr_generator_views.xml",
        "data/paper_format.xml",
        "views/lms_qr_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
