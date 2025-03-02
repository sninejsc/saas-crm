# -*- coding: utf-8 -*-

from odoo import http, fields
from odoo.tools.translate import _
from odoo.http import request, Response
from werkzeug.exceptions import InternalServerError
import json
import logging

_logger = logging.getLogger(__name__)


class ContactIntechController(http.Controller):
    @http.route('/api/lead', type='http', auth='public', methods=['POST'], cors='*', csrf=False)
    def create_crm_partner(self):
        try:
            data = json.loads(request.httprequest.data)
            _logger.info(f"Received data for CRM Opportunity creation: {data}")

            partner_data = {
                'name': data.get('name'),
                'company_name': data.get('company_name'),
                'email': data.get('email'),
                'phone': data.get('phone'),
                'comment': data.get('comment_partner'),
            }

            res_partner = request.env['res.partner'].sudo().search(
                ['|', ('email', '=', data.get('email')), ('phone', '=', data.get('phone'))], limit=1
            )

            if res_partner:
                res_partner.sudo().write(partner_data)
                msg = _('Partner %s updated successfully!' % res_partner.id)
            else:
                res_partner = request.env['res.partner'].sudo().create(partner_data)
                msg = _('Partner %s created successfully!' % res_partner.id)

            lead_data = {
                'name': _("Cơ hội của %s " % res_partner.name),
                'partner_id': res_partner.id,
                'type': data.get('type'),
                'source_partner': data.get('source_partner'),
                'description': data.get('comment_lead')
            }

            lead_id = request.env['crm.lead'].sudo().create(lead_data)
            _logger.info(f"Opportunity {lead_id.id} created successfully!, {msg}")

            return json.dumps({
                'status': 'success',
                'message': _('Opportunity %s created successfully!, %s' % (lead_id.id, msg)),
            })

        except Exception as e:
            _logger.exception(f"Error creating lead: {e}")
            raise InternalServerError(description=f'Error creating lead: {str(e)}')
