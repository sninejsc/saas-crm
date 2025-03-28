# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    def _get_next_day(self):
        today = datetime.now()
        next_day = today + timedelta(days=1)
        next_day_midnight = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
        for record in self:
            record.next_day = next_day_midnight

    def _get_crm_auto_assignmment_run_datetime(self, run_datetime, run_interval, run_interval_number):
        if not run_interval:
            return False
        if run_interval == 'manual':
            return run_datetime if run_datetime else False
        return fields.Datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + relativedelta(**{run_interval: run_interval_number})
