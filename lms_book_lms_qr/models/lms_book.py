from odoo import fields, models


class LmsBook(models.Model):
    _inherit = "lms.book"

    qr_code_id = fields.Many2one("lms.qr", string="QR Code")
    qr_code = fields.Image(related="qr_code_id.qr_code", store=True)
