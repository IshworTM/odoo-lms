from ast import literal_eval

from odoo import api, fields, models
from odoo.addons.http_routing.models.ir_http import slug


class LmsBook(models.Model):
    _name = "lms.book"
    _inherit = [
        "lms.book",
        "website.searchable.mixin",
        "website.published.multi.mixin",
    ]

    website_id = fields.Many2one("website", ondelete="cascade")
    is_published = fields.Boolean(default=True)

    @api.depends("name")
    def _compute_website_url(self):
        super(LmsBook, self)._compute_website_url()
        for book in self:
            if (
                book.id
            ):  # avoid to perform a slug on a not yet saved record in case of an onchange.
                book.website_url = "/library/book/%s" % slug(book)

    @api.model
    def _search_get_detail(self, website, order, options):
        with_image = options["displayImage"]
        with_description = options["displayDescription"]
        with_date = options["displayDetail"]
        genres = options.get("genres", "")
        languages = options.get("languages", "")
        authors = options.get("authors", "")

        domain = [website.website_domain()]
        search_genres = self.env["lms.book.genre"]
        search_languages = self.env["lms.book.language"]
        search_authors = self.env["lms.book.author"]
        mapping = {
            "name": {"name": "name", "type": "text", "match": True},
        }
        if genres:
            genre_domain, search_genres = self.search_and_append_domain(
                domain, "genres", "genre_ids", options, search_genres
            )
            if search_genres:
                domain.append(genre_domain)
        if languages:
            language_domain, search_languages = self.search_and_append_domain(
                domain, "languages", "language_id", options, search_languages
            )
            if search_languages:
                domain.append(language_domain)
        if authors:
            author_domain, search_authors = self.search_and_append_domain(
                domain, "authors", "author_ids", options, search_authors
            )
            if search_authors:
                domain.append(author_domain)
        search_fields = ["name"]
        fetch_fields = ["name", "website_url"]
        mapping = {
            "name": {"name": "name", "type": "text", "match": True},
            "website_url": {"name": "website_url", "type": "text", "truncate": False},
        }
        if with_description:
            mapping["description"] = {"name": "subtitle", "type": "text", "match": True}
        if with_date:
            mapping["detail"] = {"name": "range", "type": "html"}
        if with_image:
            mapping["image_url"] = {"name": "image_url", "type": "html"}
        return {
            "model": "lms.book",
            "base_domain": domain,
            "search_fields": search_fields,
            "fetch_fields": fetch_fields,
            "search_genres": search_genres,
            "search_languages": search_languages,
            "search_authors": search_authors,
            "mapping": mapping,
            "icon": "fa-book",
        }

    def search_and_append_domain(
        self, domain, option_name, field_name, options, model_class
    ):
        if options.get(option_name):
            try:
                ids = literal_eval(options[option_name])
            except SyntaxError:
                pass
            else:
                records = model_class.search([("id", "=", ids)])
                return ([(field_name, "in", records.ids)], records)

    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        with_image = "image_url" in mapping
        results_data = super()._search_render_results(
            fetch_fields, mapping, icon, limit
        )
        for _, data in zip(self, results_data):
            if with_image:
                data["image_url"] = "/web/image/lms.book/%s/image" % data["id"]
        return results_data


class LmsBookLanguage(models.Model):
    _inherit = "lms.book.language"

    is_published = fields.Boolean(default=False)
