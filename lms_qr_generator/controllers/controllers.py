from odoo import http
from odoo.http import request
from odoo.exceptions import UserError


class QrCode(http.Controller):
    @http.route("/lms_qr_code/read/<string:serial_no>", auth="user")
    def index(self, **kwargs):
        base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")
        qr = request.env["lms.qr"].search([("serial_no", "=", kwargs.get("serial_no"))])
        book = request.env["lms.book"].search([("qr_code_id", "=", qr.id)])
        book_action = request.env.ref("lms_book.lms_book_window_action").id
        menu_id = request.env.ref("lms_book.lms_book_menu").id
        if book:
            url = f"{base_url}/web#action={book_action}&menu_id={menu_id}&id={book.id}&model={qr.qr_generator_id.qr_type.model_id.sudo().model}&view_type=form"
        else:
            url = f"{base_url}/web#action={book_action}&menu_id={menu_id}&model={qr.qr_generator_id.qr_type.model_id.sudo().model}&view_type=form"
        return request.redirect(url)
