from datetime import datetime

from odoo import fields, models


class LmsBook(models.Model):
    _inherit = "lms.book"

    issue_ids = fields.One2many("lms.book.issue", "book_id", string="Book Issues")
    issue_history_count = fields.Integer(
        compute="_compute_issue_history_count", string="Issue History Count"
    )

    def _compute_issue_history_count(self):
        for book in self:
            book.issue_history_count = len(book.issue_ids)

    def action_check_in_book(self):
        for book in self:
            issue = book.issue_ids.filtered(lambda record: record.state != "returned")
            if issue:
                issue.returned_date = datetime.today()

    def action_book_issue_view(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "lms_book_issue.lms_book_issue_action"
        )
        if action:
            action.update(
                context=dict(
                    self.env.context, default_book_id=self.id, is_book_view=True
                ),
                target="new",
            )
            return action

    def return_action_to_open(self):
        """
        To open action while clicking in the button box,
        gets external id from context
        """
        self.ensure_one()
        xml_id = self.env.context.get("xml_id")
        if xml_id:
            res = self.env["ir.actions.act_window"]._for_xml_id(xml_id)
            res.update(
                context=dict(self.env.context, default_book_id=self.id, group_by=False),
                domain=[("book_id", "=", self.id)],
            )
            return res
        return False
