# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    state = fields.Selection([
        ('working', 'Working'),
        ('leave', 'Leave'),
    ], string='State', default='working')
    degree_ids = fields.One2many("hr.employee.degree", "employee_id", string="Degrees")
    code = fields.Char(string='Employee Code', readonly=False, copy=False)

    def action_import(self):
        domain = [('employee_id', '=', self.id)]

        action = {
            'type': 'ir.actions.act_window',
            'name': (_("Resume %s") % self.name),
            'views': [(self.env.ref('intech_hrm.hr_resume_line_tree_view').id, 'list'), (self.env.ref('hr_skills.resume_line_view_form').id, 'form')],
            'view_mode': 'tree,form',
            'res_model': 'hr.resume.line',
            'domain': domain,
            'target': 'current',
            'context': {'default_employee_id': self.id}
        }
        return action

    @api.model
    def create(self, vals):
        if not vals.get('code'):
            self._update_sequence()
            vals['code'] = self.env['ir.sequence'].next_by_code('sequence.code.employee').upper()
        return super(HrEmployee, self).create(vals)

    def write(self, vals):
        for record in self:
            if not record.code and not vals.get('code'):
                record._update_sequence()
                vals['code'] = self.env['ir.sequence'].next_by_code('sequence.code.employee').upper()
        if not vals.get('code') and len(self) == 1:
            vals['code'] = self.code

        return super(HrEmployee, self).write(vals)

    def _update_sequence(self):
        self.env.cr.execute("""
                    SELECT MAX(CAST(SUBSTRING(code FROM 3) AS INTEGER))
                    FROM hr_employee
                    WHERE code ILIKE 'IT%' AND code ~ '^IT[0-9]+'
                """)
        result = self.env.cr.fetchone()
        if result and result[0]:
            largest_number = result[0]
            sequence = self.env['ir.sequence'].search([('code', '=', 'sequence.code.employee')], limit=1)
            if sequence:
                sequence.sudo().write({'number_next': largest_number + 1})
            else:
                raise ValidationError(_("Cannot find 'sequence.code.employee' sequence to update."))

    @api.constrains('code')
    def _check_unique_employee_code(self):
        for record in self:
            if record.code and self.env['hr.employee'].search_count([
                ('code', '=', record.code),
                ('id', '!=', record.id)
            ]) > 0:
                raise ValidationError(_("Employee code '%s' already exists.") % record.code)
