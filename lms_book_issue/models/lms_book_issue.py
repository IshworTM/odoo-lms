from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class LmsBookIssue(models.Model):
    _name = "lms.book.issue"
    _description = "LMS Book Issue"
    _order = "id desc"
    _rec_name = "member_id"

    book_id = fields.Many2one(
        "lms.book", string="Book", required=True, domain="[('state','=','not_issued')]"
    )
    member_id = fields.Many2one("lms.member", string="Member", required=True)
    member_state_not_returned = fields.Boolean(
        compute="_compute_member_state_not_returned"
    )
    issued_date = fields.Date(
        string="Issued Date", default=lambda r: datetime.today(), required=True
    )
    return_date = fields.Date(
        string="Return Date",
        required=True,
        compute="_compute_return_date",
        readonly=False,
        store=True,
    )
    returned_date = fields.Date(string="Returned Date")
    state = fields.Selection(
        selection=[
            ("issued", "Issued"),
            ("overdue", "Overdue"),
            ("returned", "Returned"),
        ],
        default="issued",
    )
    due_date_display = fields.Char(
        string="Due Date", compute="_compute_due_date_display"
    )

    @api.depends("member_id")
    @api.onchange("member_id")
    def _compute_member_state_not_returned(self):
        for issue in self:
            member_issued = issue.member_id
            if member_issued:
                issue.member_state_not_returned = (
                    True
                    if member_issued.issue_ids.filtered(
                        lambda rec: rec.state != "returned"
                    )
                    else False
                )
            else:
                issue.member_state_not_returned = False

    @api.depends("issued_date")
    def _compute_return_date(self):
        for record in self:
            if record.issued_date:
                return_days = int(
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("lms.lms_book_issue_return_days")
                )
                record.return_date = record.issued_date + timedelta(days=return_days)
            else:
                record.return_date = False

    @api.constrains("issued_date")
    def validate_issue_book_date(self):
        for record in self:
            if record.issued_date:
                if record.return_date < record.issued_date:
                    raise UserError(
                        _("The return date cannot be earlier than issue date")
                    )

    @api.depends("return_date", "returned_date")
    def _compute_due_date_display(self):
        for issue in self:
            if not issue.returned_date:
                dt_return_date = issue.return_date
                dt_todays_date = datetime.today().date()
                date_diff = (dt_return_date - dt_todays_date).days
                days_var = "Day" if abs(date_diff) == 1 else "Days"
                if (date_diff) > 30:
                    issue.due_date_display = dt_return_date
                elif date_diff < -30:
                    issue.due_date_display = dt_return_date
                    issue.state = "overdue"
                elif date_diff > 0:
                    issue.due_date_display = f"{date_diff} {days_var} Left"
                    issue.state = "issued"
                elif date_diff < 0:
                    issue.due_date_display = f"{abs(date_diff)} {days_var} Ago"
                    issue.state = "overdue"
                else:
                    issue.due_date_display = "Today"
            else:
                issue.due_date_display = ""

    def action_view_new_issue_form(self):
        return (
            self.env["ir.actions.act_window"]
            .with_context({"active_id": self.id})
            ._for_xml_id("lms_book_issue.lms_book_issue_action")
        )

    def _set_book_status(self):
        for issue in self:
            book = issue.book_id
            if book:
                if book.state == "issued":
                    book.state = "not_issued"
                    issue.state = "returned"
                else:
                    book.state = "issued"

    def action_check_in_book(self):
        for issue in self:
            if issue.book_id:
                if issue.book_id.state == "not_issued":
                    raise UserError(_("This book has already been returned!"))

                issue.returned_date = datetime.today()
                if issue.returned_date:
                    return {
                        "type": "ir.actions.client",
                        "tag": "display_notification",
                        "params": {
                            "type": "success",
                            "message": _("Book successfully checked in! Thank you!"),
                            "sticky": False,
                        },
                    }

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res._set_book_status()
        return res

    def write(self, vals):
        res = super().write(vals)
        if "returned_date" in vals:
            self._set_book_status()
        return res
