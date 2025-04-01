# -*- coding: utf-8 -*-
import re
import json
import requests
import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class HrAppraisal(models.Model):
    _inherit = "hr.appraisal"

    is_check_feedback = fields.Boolean(string="Check Feedback", default=False)
    survey_user_input_ids = fields.One2many('survey.user_input', 'appraisal_id')
    feedback_status = fields.Selection([
        ('pending', 'Not Feedback'),
        ('done', 'Responded'),
        ('edit', 'Edited'),
    ], string='Feedback Status', default='pending', compute='_compute_feedback_status', store=True)

    def _get_employee_feedback_template(self):
        survey_user_input = self.env['survey.user_input'].search(
            [('appraisal_id', '=', self.id), ('partner_id', '=', self.employee_id.user_id.partner_id.id),
             ('state', '=', 'done')], limit=1)
        parts = set(line.page_id.title for line in survey_user_input.user_input_line_ids)
        totals = {part: 0 for part in parts}
        for line in survey_user_input.user_input_line_ids:
            if line.page_id.title in totals:
                totals[line.page_id.title] += line.answer_score
        totals_list = [{'title': key, 'score': value} for key, value in totals.items()]
        totals_list_sorted = sorted(
            totals_list,
            key=lambda x: int(re.match(r'^\d+', x['title']).group())
        )
        total_score = sum(value for value in totals.values())
        scoring_percentage = survey_user_input.scoring_percentage
        config_value = self.env['ir.config_parameter'].sudo().get_param('appraisal_ranges')
        appraisal_ranges = json.loads(config_value)
        type_appraisal = next(
            (label for lower, upper, label in appraisal_ranges if lower <= scoring_percentage < upper), "")
        return self.env['ir.qweb']._render('s_appraisal.hr_appraisal_employee_feedback_custom',
                                           values={'object': self, 'totals': totals_list_sorted,
                                                   'scoring_percentage': survey_user_input.scoring_percentage,
                                                   'total_score': total_score, 'type_appraisal': type_appraisal})

    def _get_manager_feedback_template(self):
        survey_user_input = self.env['survey.user_input'].search(
            [('appraisal_id', '=', self.id), ('partner_id', '=', self.manager_ids[0].user_id.partner_id.id),
             ('state', '=', 'done')], limit=1)
        parts = set(line.page_id.title for line in survey_user_input.user_input_line_ids)
        totals = {part: 0 for part in parts}
        for line in survey_user_input.user_input_line_ids:
            if line.page_id.title in totals:
                totals[line.page_id.title] += line.answer_score
        totals_list = [{'title': key, 'score': value} for key, value in totals.items()]
        totals_list_sorted = sorted(
            totals_list,
            key=lambda x: int(re.match(r'^\d+', x['title']).group())
        )
        total_score = sum(value for value in totals.values())
        scoring_percentage = survey_user_input.scoring_percentage
        config_value = self.env['ir.config_parameter'].sudo().get_param('appraisal_ranges')
        appraisal_ranges = json.loads(config_value)
        type_appraisal = next(
            (label for lower, upper, label in appraisal_ranges if lower <= scoring_percentage < upper), "")
        return self.env['ir.qweb']._render('s_appraisal.hr_appraisal_manager_feedback_custom',
                                           values={'object': self, 'totals': totals_list_sorted,
                                                   'scoring_percentage': survey_user_input.scoring_percentage,
                                                   'total_score': total_score, 'type_appraisal': type_appraisal})

    def action_feedback_results(self):
        if self.completed_survey_count < 1:
            raise UserError(_('There are no reviews yet. Please review!!!'))
        for appraisal in self.filtered(lambda a: a.state in ['new', 'pending']):
            if appraisal.state == 'pending':
                appraisal.employee_feedback = self._get_employee_feedback_template()
                appraisal.manager_feedback = self._get_manager_feedback_template()
                appraisal.is_check_feedback = True

    def _check_access(self, fields):
        pass

    def action_schat(self, employee_id):
        is_check_schat = self.env['ir.config_parameter'].sudo().get_param('soon_base.is_check_send_schat')
        if (is_check_schat):
            base_url = self.env['ir.config_parameter'].sudo().get_param('soon_base.sne_url')
            url_domain = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            token = self.env['ir.config_parameter'].sudo().get_param('ohrm_hr_update.token')
            user_send_salary = self.env['ir.config_parameter'].sudo().get_param('ohrm_hr_update.user_send_salary')
            id_user_reward = self._get_user(employee_id.user_id.user_schat, base_url, token)
            id_channel = self._get_chanel_user(user_send_salary, id_user_reward, base_url, token)
            if id_user_reward != 'app.user.get_by_username.app_error' or id_channel != 'api.context.invalid_body_param.app_error':
                self._post_message(id_channel, base_url, token, employee_id.user_id.name, employee_id, url_domain)

    def _get_user(self, user_schat, base_url, token):
        try:
            url = f"{base_url}/users/username/{user_schat}"
            payload = {}
            headers = {
                'Authorization': token
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            return response.json().get('id')
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error fetching user: {e}")
            return None

    def _get_chanel_user(self, user_send, user_reward, base_url, token):
        try:
            url = f"{base_url}/channels/direct"
            payload = json.dumps([
                user_send,
                user_reward
            ])
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, data=payload)
            return response.json().get('id')
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error creating channel: {e}")
            return None

    def _post_message(self, channel_id, base_url, token, user, employee_id, url_domain):
        try:
            survey_user_input = self.env['survey.user_input'].search(
                [('appraisal_id', '=', self.id), ('partner_id', '=', employee_id.user_id.partner_id.id)], limit=1)
            url = survey_user_input.get_start_url()
            payload = {
                "channel_id": channel_id,
                "message": f'Kính gửi {user},\n' +
                           f'Bản đánh giá cuối năm dành cho nhân viên {self.employee_id.name}, phòng {self.employee_id.department_id.name} đang được hoàn thiện.\n' +
                           f'Bạn vui lòng truy cập vào đường dẫn dưới đây để hoàn tất quá trình đánh giá:\n[Link đánh giá]({url_domain}{url})\n\n' +
                           'Trân trọng cảm ơn!'
            }
            headers = {
                'Content-Type': 'application/json',
                'Authorization': token
            }
            response = requests.post(f'{base_url}/posts', headers=headers, data=json.dumps(payload))
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error posting message: {e}")
            return None

    def action_hr_appraisal_radar_chart(self):
        self.ensure_one()
        chart_data = self._get_data_for_radar_chart()

        return {
            'type': 'ir.actions.client',
            'tag': 's_appraisal.hr_appraisal_radar_chart',
            'name': _('Appraisal Radar Chart'),
            'context': {
                'data': chart_data
            },
        }

    def _get_data_for_radar_chart(self):
        self.ensure_one()

        survey_user_inputs = self.env['survey.user_input'].search(
            [('appraisal_id', '=', self.id), ('state', '=', 'done')]
        )

        if not survey_user_inputs:
            return [{'name': '', 'labels': [], 'scores': []}]

        result = []

        for survey_user_input in survey_user_inputs:
            parts = set(line.page_id.title for line in survey_user_input.user_input_line_ids)
            totals = {part: 0 for part in parts}

            for line in survey_user_input.user_input_line_ids:
                if line.page_id.title in totals:
                    totals[line.page_id.title] += line.answer_score

            totals_list = [{'title': key, 'score': value} for key, value in totals.items()]
            totals_list_sorted = sorted(
                totals_list,
                key=lambda x: int(re.match(r'^\d+', x['title']).group()) if re.match(r'^\d+', x['title']) else float(
                    'inf')
            )

            labels = [item['title'] for item in totals_list_sorted]
            scores = [item['score'] for item in totals_list_sorted]

            result.append({
                'name': survey_user_input.nickname,
                'labels': labels,
                'scores': scores
            })

        return result

    def action_do_appraisal(self):
        self.ensure_one()
        if not self.survey_user_input_ids:
            raise UserError(_("There are no surveys associated with this review."))

        employee_id = self.employee_id.id if self.employee_id else False
        survey_input = self.env['survey.user_input'].search([
            ('appraisal_id', '=', self.id),
            ('employee_id', '=', employee_id),
            ('state', '=', 'new'),
            ('partner_id', '=', self.env.user.partner_id.id)
        ], limit=1)

        if survey_input.state == 'done' or survey_input.state == 'in_progress' or not survey_input:
            raise UserError(_("This survey has been or is being conducted."))

        manager_ids = self.manager_ids
        if self.env.user.id not in manager_ids.mapped('user_id').ids and self.env.user.id != self.employee_id.user_id.id:
            raise UserError(_("You do not have access to this survey."))

        survey_url = survey_input.get_start_url()
        return {
            'name': _('Open Appraisal'),
            'type': 'ir.actions.act_url',
            'target': 'current',
            'url': survey_url,
        }

    @api.depends('survey_user_input_ids.state', 'survey_user_input_ids.is_edit')
    def _compute_feedback_status(self):
        for record in self:
            if not record.survey_user_input_ids:
                record.feedback_status = 'pending'
            else:
                if any(survey.is_edit == True for survey in record.survey_user_input_ids):
                    record.feedback_status = 'edit'
                elif any(survey.state == 'new' for survey in record.survey_user_input_ids):
                    record.feedback_status = 'pending'
                else:
                    record.feedback_status = 'done'
