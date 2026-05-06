try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
import datetime
from io import BytesIO

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from PIL import Image


class LmsQr(models.Model):
    _name = "lms.qr"
    _description = "LMS QR"
    _rec_name = "serial_no"

    serial_no = fields.Char(string="Serial No.")
    qr_code = fields.Binary("QRcode")
    qr_generator_id = fields.Many2one("lms.qr.generator", string="QR Generator")

    def _generate_serial_no(self, qr_type_name):
        recent_serial = self.search([], order="id desc", limit=1, offset=1)
        if recent_serial and (self._is_created_today(recent_serial)):
            recent_serial_no = recent_serial.serial_no
            serial_no_parts = recent_serial_no.split("-")
            serial_no_parts[0] = "".join(
                word[0] for word in qr_type_name.split()
            ).upper()
            serial_no_parts[-1] = str(int(serial_no_parts[-1]) + 1)
            serial_no = "-".join(serial_no_parts)
            return serial_no
        else:
            return self._create_new_serial_no(qr_type_name)

    def _is_created_today(self, serial_no):
        return serial_no.create_date.date() == datetime.date.today()

    def _create_new_serial_no(self, qr_type_name):
        if qr_type_name:
            qr_serial_initials = "".join(
                word[0] for word in qr_type_name.split()
            ).upper()
            current_date = datetime.datetime.now().strftime("-%y-%m-%d")
            return f"{qr_serial_initials}{current_date}-1"

    def _compute_generate_qr(self):
        "Method to generate QR code"
        for rec in self:
            qr_generator = rec.qr_generator_id
            logo = Image.open("addons_lms/lms_qr_generator/static/src/images/logo.png")
            basewidth = qr_generator.image_base_width
            wpercent = basewidth / float(logo.size[0])
            hsize = int(float(logo.size[1]) * float(wpercent))
            try:
                resample_filter = Image.ANTIALIAS
            except AttributeError:
                resample_filter = Image.Resampling.LANCZOS
            logo = logo.resize((basewidth, hsize), resample_filter)
            base_url = self.env["ir.config_parameter"].get_param("web.base.url")
            if qr_generator.qr_type.qr_type == "table":
                url = f"{base_url}/library"
            else:
                url = f"{base_url}/lms_qr_code/read/{rec.serial_no}"
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=qr_generator.qr_box_size,
                    border=qr_generator.qr_border,
                )
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image(
                    fill_color=qr_generator.color,
                    back_color=qr_generator.back_color,
                ).convert("RGB")
                pos = (
                    (img.size[0] - logo.size[0]) // 2,
                    (img.size[1] - logo.size[1]) // 2,
                )
                img.paste(logo, pos)
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                return qr_image
            else:
                raise UserError(
                    _("Necessary Requirements To Run This Operation Is Not Satisfied")
                )

    @api.model_create_multi
    def create(self, vals_list):
        qrs = super().create(vals_list)
        for qr in qrs:
            if qr.qr_generator_id.qr_type.qr_type != "table":
                qr.serial_no = qr._generate_serial_no(qr.qr_generator_id.qr_type.name)
            qr.qr_code = qr._compute_generate_qr()
        return qrs
