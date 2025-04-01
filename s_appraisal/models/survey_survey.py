# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Survey(models.Model):
    _inherit = 'survey.survey'

    def action_return_appraisal(self, answer_token):
        user_input = self.env['survey.user_input'].search([
            ('survey_id', '=', self.id),
            ('appraisal_id', '!=', False),
            ('partner_id', '=', self.env.user.partner_id.id),
            ('access_token', '=', answer_token),
        ], limit=1)

        if not user_input:
            raise UserError(_("No Appraisal linked to this survey."))

        return {
            'res_id': user_input.appraisal_id.id,
        }

    def action_survey_user_input_completed(self):
        action = super(Survey, self).action_survey_user_input_completed()
        ctx = action.get('context', {})
        ctx.update({
            'search_default_group_by_reviewed_employees': True
        })
        action['context'] = ctx
        return action
