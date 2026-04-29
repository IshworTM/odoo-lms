import logging

from odoo import http
from odoo.addons.portal.controllers.portal import pager
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request

logger = logging.getLogger(__name__)


class LibraryMenu(http.Controller):
    @http.route(
        ["/library", "/library/page/<int:page>"],
        type="http",
        auth="public",
        website=True,
    )
    def books(self, page=1, **searches):
        searches.setdefault("search", "")
        searches.setdefault("genres", "")
        searches.setdefault("languages", "")
        searches.setdefault("authors", "")
        step = 24
        lms_book = request.env["lms.book"]
        website = request.website
        order = "id desc"

        options = {
            "displayDescription": False,
            "displayDetail": False,
            "displayExtraDetail": False,
            "displayExtraLink": False,
            "displayImage": False,
            "allowFuzzy": not searches.get("noFuzzy"),
            "genres": searches.get("genres"),
            "languages": searches.get("languages"),
            "authors": searches.get("authors"),
        }

        search = searches.get("search")
        book_count, details, fuzzy_search_term = website._search_with_fuzzy(
            "library", search, limit=page * step, order=order, options=options
        )
        book_details = details[0]
        books = book_details.get("results", lms_book)
        books = books[(page - 1) * step : page * step]
        search_genres = book_details["search_genres"]
        search_languages = book_details["search_languages"]
        search_authors = book_details["search_authors"]

        author_count = len(set(lms_book.search([]).mapped("author_ids")))
        genre_count = len(set(lms_book.search([]).mapped("genre_ids")))

        # pagination
        page_detail = pager(url="/library", total=book_count, page=page, step=24)

        statistics = [
            {"label": "Total Books", "value": book_count},
            {"label": "Total Authors", "value": author_count},
            {"label": "Total Genres", "value": genre_count},
        ]
        keep = QueryURL(
            "/library",
            **{key: value for key, value in searches.items() if (key == "search")},
        )

        return request.render(
            "lms_website_book.library_index",
            {
                "statistics": statistics,
                "book_ids": books,
                "book_languages": request.env["lms.book.language"].search(
                    [("is_published", "=", True)]
                ),
                "genres": request.env["lms.book.genre"].search([]),
                "authors": request.env["lms.book.author"].search([]),
                "pager": page_detail,
                "search_genres": search_genres,
                "search_languages": search_languages,
                "search_authors": search_authors,
                "searches": searches,
                "search_count": book_count,
                "keep": keep,
                "original_search": fuzzy_search_term and search,
            },
        )

    @http.route(
        ['/library/book/<model("lms.book"):book>'],
        type="http",
        auth="public",
        website=True,
    )
    def library_book_template(self, book):
        accordion_items = [
            {
                "id": "tabular_book_details",
                "title": "Book Details",
                "expanded": True,
                "template": "lms_website_book.lms_book_information",
            },
            {
                "id": "additional_book_details",
                "title": "Additional Details",
                "expanded": False,
                "template": "lms_website_book.lms_book_additional_details",
            },
            {
                "id": "author_book_details",
                "title": "Author Details",
                "expanded": False,
                "template": "lms_website_book.lms_book_author_details",
            },
            {
                "id": "lms_author_top_book_container",
                "title": "Top Books By Author(s)",
                "expanded": False,
                "template": "lms_website_book.lms_author_top_books",
            },
            {
                "id": "book_description",
                "title": "Synopsis",
                "expanded": False,
                "template": "lms_website_book.lms_book_synopsis",
            },
        ]
        book_issue_count = [
            {
                "id": author_book.id,
                "name": f"{author_book.name}",
                "count": len(author_book.issue_ids),
            }
            for author_book in book.author_ids.book_ids
        ]
        sorted_books = sorted(
            book_issue_count, key=lambda item: item.get("count"), reverse=True
        )
        top_books = [top_book for top_book in sorted_books[:5]]
        values = {
            "book_details": book,
            "top_book_list": top_books,
            "accordion_items": accordion_items,
        }
        return request.render("lms_website_book.book_details", values)
