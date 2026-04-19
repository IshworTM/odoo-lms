from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    lms_book_issue_return_days = fields.Integer(string="Return Days")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            lms_book_issue_return_days=int(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("lms.lms_book_issue_return_days", default=7)
            )
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "lms.lms_book_issue_return_days", self.lms_book_issue_return_days
        )
