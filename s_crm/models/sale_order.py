# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def read(self, fields=None, load='_classic_read'):
        if self.env.user.partner_id in self.message_follower_ids.mapped('partner_id'):
            self = self.sudo()

        if self.env.user.has_group('intech_crm.group_sbu_manager'):
            if self.env.user.company_id.id in self.env.user.company_ids.ids:
                self = self.sudo()
        return super(SaleOrder, self).read(fields, load)
