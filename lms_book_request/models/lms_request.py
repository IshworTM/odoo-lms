from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class LmsBookRequest(models.Model):
    _name = "lms.book.request"
    _description = "Book Requests"

    name = fields.Char(string="Book Name", required=True)
    genre = fields.Char(string="Genre")
    author = fields.Char(string="Author Name")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(related="company_id.currency_id")
    price = fields.Monetary(string="MRP", currency_field="company_currency_id")
    publisher = fields.Char(string="Publisher")
    language = fields.Char(string="Language")

    @api.constrains("name")
    def _constrains_unique_name(self):
        """
        Ensures that each book requested in the `lms.book.request` model has a unique name.

        This method checks if a book with the same name already exists within the `lms.book.request` model,
        except for the current record being processed. If a duplicate is found, it raises
        a `ValidationError`.

        This method uses the following logic:
        - Searches for other requests with the same book name (`name`) but a different record ID (`id`).
        - If such a request is found, it raises a `ValidationError` with a message indicating that the
        book has already been requested.

        Raises:
            ValidationError: If a duplicate book name is found in other requests.

        Example:
            >>> request = env['lms.book.request'].create({'name': 'Sample Book'})
            >>> # The above creation will be allowed.
            >>> duplicate_request = env['lms.book.request'].create({'name': 'Sample Book'})
            >>> # The above creation will raise a ValidationError because 'Sample Book' already exists.
        """
        for request in self:
            other_requests = self.env["lms.book.request"].search(
                [("name", "=", request.name), ("id", "!=", request.id)]
            )
            if other_requests:
                raise ValidationError(
                    _(f'The book "{request.name}" has already been requested!!')
                )
