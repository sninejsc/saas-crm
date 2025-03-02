/** @odoo-module **/
import {session} from "@web/session";
import { useService } from '@web/core/utils/hooks';
import { patch } from "@web/core/utils/patch";
import { makeContext } from "@web/core/context";
import { _t } from "@web/core/l10n/translation";

import { X2ManyField } from "@web/views/fields/x2many/x2many_field";

patch(X2ManyField.prototype,{
    setup() {
        super.setup();
    },

     async onAdd({ context, editable } = {}) {
        const customContext = {
            default_city: false,
            default_country_id: false,
            default_state_id: false,
            default_street: false,
            default_street2: false,
            default_zip: false,
        };
        const domain =
            typeof this.props.domain === "function" ? this.props.domain() : this.props.domain;
        context = makeContext([this.props.context,customContext, context]);
        if (this.isMany2Many) {
            const { string } = this.props;
            const title = _t("Add: %s", string);
            return this.selectCreate({ domain, context, title });
        }
        if (editable) {
            if (this.list.editedRecord) {
                const proms = [];
                this.list.model.bus.trigger("NEED_LOCAL_CHANGES", { proms });
                await Promise.all([...proms, this.list.editedRecord._updatePromise]);
                await this.list.leaveEditMode({ canAbandon: false });
            }
            if (!this.list.editedRecord) {
                return this.addInLine({ context, editable });
            }
            return;
        }
        return this._openRecord({ context });
    }

});
