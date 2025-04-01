# -*- coding: utf-8 -*-

from odoo import http, fields
from odoo.tools.translate import _
from odoo.http import request, Response
from werkzeug.exceptions import InternalServerError
import json
import logging

_logger = logging.getLogger(__name__)

class SurveyCloseTab(http.Controller):

    @http.route('/survey/close_tab', type='http', auth='public', methods=['POST'], cors='*', csrf=False)
    def close_survey(self):
        data = json.loads(request.httprequest.data)
        access_token = data.get('access_token')

        if access_token:
            survey_input = request.env['survey.user_input'].sudo().search([
                ('access_token', '=', access_token),
            ], limit=1)

            if survey_input:
                survey_input.sudo().write({'state': 'done'})
