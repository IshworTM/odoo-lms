/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(WebClient.prototype, "va_lms.WebClient", {
  setup() {
    this._super.apply(this, arguments);
    this.orm = useService("orm");
    const app_title = "";
    this.title.setParts({ zopenerp: app_title });
  },
});
