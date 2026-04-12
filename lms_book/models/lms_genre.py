import ast

from odoo import _, api, fields, models


class LmsBookGenre(models.Model):
    _name = "lms.book.genre"
    _description = "Lms Book Genre"

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
    book_ids = fields.Many2many("lms.book", string="Books")
    total = fields.Integer(compute="_compute_total_books")

    _sql_constraints = [
        ("check_unique_name", "unique(name)", "The name of the genre must be unique.")
    ]

    @api.depends("book_ids")
    def _compute_total_books(self):
        for record in self:
            record.total = len(record.book_ids)

    def action_book_genre(self):
        action = (
            self.env["ir.actions.act_window"]
            .with_context({"active_id": self.id})
            ._for_xml_id("lms_book.lms_book_window_action")
        )
        action["display_name"] = _(f"{self.name} Books", name=self.name)
        context = action["context"].replace("active_id", str(self.id))
        context = ast.literal_eval(context)
        context.update({"default_genre_ids": self.ids})
        action["context"] = context
        action["domain"] = [("id", "=", self.book_ids.ids)]
        return action
