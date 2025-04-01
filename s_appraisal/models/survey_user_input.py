# -*- coding: utf-8 -*-

import logging
import requests
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


_logger = logging.getLogger(__name__)

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    manager_ids = fields.Many2many('res.users', compute='_compute_manager_ids')
    employee_id = fields.Many2one('hr.employee', string="Employee", compute="_compute_employee", store=True)
    is_state_appraisal = fields.Boolean(compute="_compute_is_state_appraisal")
    is_edit = fields.Boolean(default=False, store=True)


    def _save_lines(self, question, answer, comment=None, overwrite_existing=True):
        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])
        overwrite_existing = True
        if old_answers and not overwrite_existing:
            raise UserError(_("This answer cannot be overwritten."))

        if question.question_type in ['char_box', 'text_box', 'numerical_box', 'date', 'datetime']:
            self._save_line_simple_answer(question, old_answers, answer)
            if question.save_as_email and answer:
                self.write({'email': answer})
            if question.save_as_nickname and answer:
                self.write({'nickname': answer})

        elif question.question_type in ['simple_choice', 'multiple_choice']:
            self._save_line_choice(question, old_answers, answer, comment)
        elif question.question_type == 'matrix':
            self._save_line_matrix(question, old_answers, answer, comment)
        else:
            raise AttributeError(question.question_type + ": This type of question has no saving function")

    def action_edit_survey_inputs(self):
        try:
            manager_ids = self.appraisal_id.manager_ids
            if self.env.user.id in manager_ids.mapped('user_id').ids or self.env.user.id == self.create_uid:
                self.state = 'in_progress'
                self.is_edit = True
                url = self.get_start_url()
            else:
                raise UserError(_("You don't have permission to edit this appraisal."))

            return {
                'name': _('Review Answers'),
                'type': 'ir.actions.act_url',
                'target': 'current',
                'url': url,
            }

        except requests.exceptions.RequestException as e:
            _logger.warning(e)

    @api.depends("appraisal_id.manager_ids")
    def _compute_manager_ids(self):
        for record in self:
            if record.appraisal_id:
                record.manager_ids = record.appraisal_id.manager_ids.mapped("user_id")

    @api.depends("appraisal_id.employee_id")
    def _compute_employee(self):
        for record in self:
            record.employee_id = record.appraisal_id.employee_id if record.appraisal_id else False

    @api.depends('appraisal_id.state')
    def _compute_is_state_appraisal(self):
        for record in self:
            record.is_state_appraisal = record.appraisal_id.state == 'done'
