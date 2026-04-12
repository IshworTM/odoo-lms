from odoo import api, fields, models


class LmsBookAuthor(models.Model):
    _name = "lms.book.author"
    _description = "Lms Book author"

    name = fields.Char(required=True)
    color = fields.Char(string="color", default="4")
    book_ids = fields.Many2many("lms.book")
    country_id = fields.Many2one(
        "res.country",
        string="Country",
        compute="_compute_author_country",
        required=True,
        store=True,
        readonly=False,
    )
    book_count = fields.Integer(string="Total books", compute="_compute_book_count")
    language_id = fields.Many2one(
        "lms.book.language",
        string="Language",
        compute="_compute_author_language",
        required=True,
        store=True,
        readonly=False,
    )

    _sql_constraints = [
        (
            "check_unique_author",
            "unique(name)",
            "The name of the author must be unique.",
        )
    ]

    @api.depends("book_ids")
    def _compute_author_country(self):
        for author in self:
            if not author.country_id:
                if author.book_ids:
                    author.country_id = author.book_ids[0].country_id
                else:
                    author.country_id = None

    @api.depends("book_ids")
    def _compute_book_count(self):
        for author in self:
            author.book_count = len(author.book_ids)

    @api.depends("book_ids")
    def _compute_author_language(self):
        for author in self:
            if not author.language_id:
                author.language_id = None
                if author.book_ids:
                    for book in author.book_ids:
                        if not book.is_translated and book.language_id:
                            author.language_id = book.language_id
                        elif book.is_translated and book.translated_from:
                            author.language_id = book.translated_from
