from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    member_id = fields.Many2one("lms.member", string="Library Member")
