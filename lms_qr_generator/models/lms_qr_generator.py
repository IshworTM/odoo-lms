import base64
from datetime import datetime

from odoo import api, fields, models


class LmsQrGenerator(models.Model):
    _name = "lms.qr.generator"
    _description = "Lms Qr Generator"

    name = fields.Char(compute="_compute_name", store=True)
    qr_type = fields.Many2one("lms.qr.type", string="QR Type")
    quantity = fields.Integer(string="Quantity")
    qr_ids = fields.One2many("lms.qr", "qr_generator_id", string="QR")
    qr_box_size = fields.Integer(string="QR Box Size", default="4")
    qr_border = fields.Integer(string="QR Border", default="3")
    color = fields.Char("QR Color", default="#000")
    back_color = fields.Char("Background Color", default="#fff")
    image = fields.Image(string="Qr Logo Image")
    image_base_width = fields.Integer(string="Image Base Width", default="60")
    state = fields.Selection(
        selection=[("not_generated", "Not Generated"), ("generated", "Generated")],
        default="not_generated",
    )

    @api.depends("qr_type")
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.qr_type.name} QR generated on {datetime.now().date()}"

    def generate_qr(self):
        for rec in self:
            for _ in range(rec.quantity):
                rec.write({"qr_ids": [(0, 0, {})]})
            rec.state = "generated"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for vals in vals_list:
            if "image" in vals:
                self.create_logo(res.image)
        return res

    def create_logo(self, logo):
        """Creates Logo in Required directory of particular instance

        Args:
            logo (binary): The logo selected on the form view
        """
        decoded_image_data = base64.b64decode(logo)
        file_path = f"addons_lms/lms_qr_generator/static/src/images/logo.png"
        with open(file_path, "wb") as file:
            file.write(decoded_image_data)


class LmsQrType(models.Model):
    _name = "lms.qr.type"
    _description = "Lms Qr Type"

    name = fields.Char(required=True)
    model_id = fields.Many2one("ir.model", string="Model")
    qr_type = fields.Selection(
        selection=[("book", "Book"), ("member", "Member"), ("table", "Table")],
        required=True,
    )
