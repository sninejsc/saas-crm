# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.fields import Datetime
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    code_partner = fields.Char(string='Code Partner', readonly=False, copy=False)

    group_id = fields.Many2one(comodel_name='crm.data', domain="[('type', '=', 'group')]", string='Group Partner')
    source_id = fields.Many2one(comodel_name='crm.data', domain="[('type', '=', 'source')]", string='Source Partner')
    partner_state_id = fields.Many2one(comodel_name='crm.data', domain="[('type', '=', 'relation')]", string='Relation')
    user_id = fields.Many2one(
        'res.users', string='Salesperson',
        compute='_compute_user_id',
        precompute=True,  # avoid queries post-create
        readonly=False, store=True,
        default=lambda self: self.env.user,
        help='The internal user in charge of this contact.')
    create_date_intech = fields.Date(string='Create Date', default=fields.Date.today)
    property_account_payable_id = fields.Many2one(required=False)
    property_account_receivable_id = fields.Many2one(required=False)


    _sql_constraints = [
        ('unique_code_partner',
         'unique(code_partner)',
         "The code partner must be unique."),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('code_partner'):
            self._update_sequence()
            vals['code_partner'] = self.env['ir.sequence'].next_by_code('sequence.code.partner').upper()
        if not vals.get('create_date_intech'):
            vals['create_date_intech'] = fields.Date.today()
        if not vals.get('user_id'):
            vals['user_id'] = self.env.user.id
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        for record in self:
            if not record.code_partner and not vals.get('code_partner'):
                record._update_sequence()
                vals['code_partner'] = self.env['ir.sequence'].next_by_code('sequence.code.partner').upper()
            if not vals.get('create_date_intech'):
                vals['create_date_intech'] = fields.Date.today()
            if 'user_id' in vals and not vals.get('user_id'):
                vals['user_id'] = self.user_id.id
        if not vals.get('code_partner') and len(self) == 1:
            vals['code_partner'] = self.code_partner

        return super(ResPartner, self).write(vals)

    def _update_sequence(self):
        self.env.cr.execute("""
            SELECT MAX(CAST(SUBSTRING(code_partner FROM 3) AS INTEGER))
            FROM res_partner
            WHERE code_partner ILIKE 'KH%' AND code_partner ~ '^KH[0-9]+'
        """)
        result = self.env.cr.fetchone()
        if result and result[0]:
            largest_number = result[0]
            sequence = self.env['ir.sequence'].search([('code', '=', 'sequence.code.partner')], limit=1)
            if sequence:
                sequence.sudo().write({'number_next': largest_number + 1})
            else:
                raise ValidationError(_("Cannot find 'sequence.code.partner' sequence to update."))

    def archive_partner(self):
        for rec in self:
            rec.active = False
            rec.write({'parent_id': False})

    @api.onchange('partner_id')
    def update_contact_person(self):
        self.contact_person_id = False
