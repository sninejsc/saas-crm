# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SurveyQuestionAnswer(models.Model):
    _inherit = 'survey.question.answer'

    value = fields.Text('Suggested Value', translate=True, required=True)
