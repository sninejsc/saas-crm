# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AppraisalAskFeedback(models.TransientModel):
    _inherit = "appraisal.ask.feedback"

    is_schat = fields.Boolean(string='Send Spod', default=False)

    def action_send(self):
        if self.is_schat:
            self.ensure_one()
            answers = self._prepare_survey_anwers(self.employee_ids)
            answers.sudo().write({'appraisal_id': self.appraisal_id.id, 'deadline': self.deadline})
            for employee in self.employee_ids:
                self.appraisal_id.action_schat(employee)

            self.appraisal_id.employee_feedback_ids |= self.employee_ids
            self.appraisal_id.survey_ids |= self.survey_template_id
        else:
            return super(AppraisalAskFeedback, self).action_send()
