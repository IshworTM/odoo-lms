from datetime import datetime, timedelta

from odoo import api, fields, models


class LmsMember(models.Model):
    _name = "lms.member"
    _description = "Lms Member"
    _rec_name = "display_name"

    display_name = fields.Char(
        compute="_compute_display_name", store=True, readonly=True
    )
    member_name = fields.Char(string="Name", required=True)
    image = fields.Image(string="Image")
    address = fields.Char(string="Address")
    phone_no = fields.Char(string="Phone No.")
    email = fields.Char(string="E-mail")
    membership_type = fields.Selection(
        selection=[("silver", "Silver"), ("gold", "Gold"), ("premium", "Premium")],
        string="Membership Type",
    )
    issued_date = fields.Date(
        string="Issued Date", required=True, default=lambda r: datetime.today()
    )
    expiry_date = fields.Date(
        string="Expiry Date",
        default=lambda expiry: datetime.today() + timedelta(days=365),
        required=True,
    )
    date_of_birth = fields.Date(string="Date of Birth")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(related="company_id.currency_id")
    membership_price = fields.Monetary(
        string="Membership Price", currency_field="company_currency_id"
    )
    payment_status = fields.Selection(
        selection=[
            ("unpaid", "Unpaid"),
            ("partially_paid", "Partially Paid"),
            ("paid", "Paid"),
        ],
        string="Payment Status",
        required=True,
        default="unpaid",
    )
    partially_paid_amount = fields.Monetary(
        string="Partially Paid Amount", currency_field="company_currency_id"
    )
    partner_id = fields.Many2one("res.partner")
    unique_id = fields.Char(string="Member ID", store=True)
    active = fields.Boolean(string="Active", default=True)
    _sql_constraints = [
        ("unique_unique_id", "unique(unique_id)", "Member ID must be unique.")
    ]

    def _generate_unique_id(self, member_issued_date):
        if member_issued_date:
            issued_date = member_issued_date.strftime("%Y%m%d")
            recent_member = self.search([], order="id desc", limit=1, offset=1)
            if recent_member:
                new_member_id = recent_member.id + 1
                unique_id = f"{issued_date[4:]}{new_member_id}"
            else:
                unique_id = f"{issued_date[4:]}-1"
            return unique_id

    @api.depends("member_name", "issued_date")
    def _compute_display_name(self):
        for member in self:
            member_unique_id = member.unique_id
            member_name = member.member_name
            if member_unique_id and member_name:
                member.display_name = f"{member_unique_id}-{member_name}"
            else:
                member.display_name = None

    def _create_member_partner(self):
        for member in self:
            member.partner_id = self.env["res.partner"].create(
                {
                    "name": member.member_name,
                    "image_1920": member.image,
                    "city": member.address,
                    "phone": member.phone_no,
                    "email": member.email,
                    "member_id": member.id,
                }
            )

    @api.model_create_multi
    def create(self, vals_list):
        members = super().create(vals_list)
        members._create_member_partner()
        for member in members:
            if not member.unique_id:
                member.unique_id = self._generate_unique_id(member.issued_date)
        return members
