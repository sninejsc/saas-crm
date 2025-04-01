# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    wage = fields.Monetary(tracking=True)
    basic_salary = fields.Monetary(tracking=True)
    performance_salary = fields.Monetary(tracking=True)
    meal_allowance = fields.Monetary(tracking=True)
    fuel_allowance = fields.Monetary(tracking=True)
    other_allowance = fields.Monetary(tracking=True)
