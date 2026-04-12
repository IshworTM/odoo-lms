from odoo import fields, models


class LmsBook(models.Model):
    _name = "lms.book"
    _description = "Lms Book"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    image = fields.Image()
    name = fields.Char(required=True)
    country_id = fields.Many2one("res.country", string="Country")
    genre_ids = fields.Many2many("lms.book.genre", string="Genre")
    author_ids = fields.Many2many("lms.book.author", string="Authors")
    language_id = fields.Many2one("lms.book.language", string="Language")
    isbn = fields.Char(string="ISBN", required=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(related="company_id.currency_id")
    price = fields.Monetary(string="MRP", currency_field="company_currency_id")
    state = fields.Selection(
        selection=[("issued", "Issued"), ("not_issued", "Not Issued")],
        default="not_issued",
    )
    publisher_id = fields.Many2one("lms.book.publisher", string="Publisher")
    date_published = fields.Char(string="Date Published")
    edition = fields.Char(string="Edition")
    pages = fields.Integer(string="Pages")
    shelf_id = fields.Many2one("lms.book.shelf", string="Shelf")
    is_translated = fields.Boolean(default=False)
    translator_id = fields.Many2one("lms.book.translator", string="Translated By")
    translated_from = fields.Many2one("lms.book.language", string="Translated From")
    translated_to = fields.Many2one("lms.book.language", string="Translated To")
    is_series = fields.Boolean(string="Series", default=False)
    parent_id = fields.Many2one(
        "lms.book", domain="[('is_series', '=', True),('parent_id', '=', False)]"
    )
    child_ids = fields.One2many("lms.book", "parent_id")
    description = fields.Html(string="Synopsis")


class LmsBookPublisher(models.Model):
    _name = "lms.book.publisher"
    _description = "Lms Book Publisher"

    name = fields.Char(required=True)


class LmsBookShelf(models.Model):
    _name = "lms.book.shelf"
    _description = "Lms Book Shelf"

    name = fields.Char(required=True)


class LmsBookTranslator(models.Model):
    _name = "lms.book.translator"
    _description = "Lms Book Translator"

    name = fields.Char(required=True)


class LmsBookLanguage(models.Model):
    _name = "lms.book.language"
    _description = "Lms Book Translator"

    name = fields.Char(required=True)
