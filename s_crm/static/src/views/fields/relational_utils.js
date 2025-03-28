/** @odoo-module **/
import {session} from "@web/session";
import { useService } from '@web/core/utils/hooks';
import { patch } from "@web/core/utils/patch";

import { X2ManyFieldDialog } from "@web/views/fields/relational_utils";

patch(X2ManyFieldDialog.prototype,{
    setup() {
        super.setup();
        this.orm = useService('orm');
    },

    async archive() {
        const result = await this.orm.call(
        'res.partner',
        'archive_partner',
        [this.record.data.id]
        );
        this.props.close();
        location.reload();

    }

});
