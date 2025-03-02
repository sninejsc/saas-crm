# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.fields import Datetime
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    code_partner = fields.Char(string='Code Partner', related='partner_id.code_partner')

    name = fields.Char(
        'Opportunity', index='trigram', required=True,
        compute='_compute_name', readonly=False, store=True, translate=True)
    product_category_id = fields.Many2one('product.category', string='Product Category')
    date_create = fields.Date(string='Create Date', default=Datetime.now)
    contact_person_id = fields.Many2one('res.partner', string='Contact Person')
    contact_phone = fields.Char(related='contact_person_id.phone', string='Contact Phone')
    contact_email = fields.Char(related='contact_person_id.email', string='Contact Email')
    is_partner_person = fields.Boolean(string="Is Partner Person", compute="_compute_is_partner_person", store=True)

    source_partner = fields.Char(string="Source")

    @api.depends("partner_id")
    def _compute_is_partner_person(self):
        for record in self:
            record.is_partner_person = record.partner_id.company_type == "person" if record.partner_id else False

    @api.model
    def create(self, vals):
        if not vals.get('date_create'):
            vals['date_create'] = fields.Date.today()
        if not vals.get('user_id'):
            vals['user_id'] = self.env.user.id
        return super(CrmLead, self).create(vals)

    def write(self, vals):
        if not vals.get('date_create'):
            vals['date_create'] = fields.Date.today()
        if 'user_id' in vals and not vals.get('user_id'):
            vals['user_id'] = self.user_id.id
        return super(CrmLead, self).write(vals)

    def read(self, fields=None, load='_classic_read'):
        if self.env.user.partner_id in self.message_follower_ids.mapped('partner_id'):
            self = self.sudo()
        return super(CrmLead, self).read(fields, load)

