# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
import logging
import json
from odoo.exceptions import UserError
from requests.auth import HTTPDigestAuth
import requests, datetime
import pytz
from datetime import datetime, timedelta
from datetime import time
from dateutil.relativedelta import relativedelta
from odoo.models import NewId

_logger = logging.getLogger(__name__)


class HrLeave(models.Model):
    _name = 'hr.leave'
    _inherit = ['hr.leave', 'mail.thread', 'mail.activity.mixin','tier.validation']

    _state_field = "state"
    _state_from = ['draft', 'confirm']
    _state_to = ['validate']
    _to_approve_state = 'confirm'
    _approved_state = 'validate'
    _rejected_state = 'refuse'
    _subject_prefix = '[Leave Management System]'
    _subject_code = 'employee_id'
    _enable_restart_validation = False
    _tier_validation_manual_config = False
