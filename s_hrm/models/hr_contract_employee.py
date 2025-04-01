# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, tools

class HrContractStatusView(models.Model):
    _name = 'hr.contract.employee'
    _auto = False
    _description = 'Contract Status Employee'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    employee_name = fields.Char(string="Employee Name")
    contract_id = fields.Many2one('hr.contract', string='Latest Contract')
    contract_state = fields.Selection([
        ('draft', 'New'),
        ('open', 'Running'),
        ('close', 'Expired'),
        ('cancel', 'Cancelled'),
    ], string='Contract State')
    contract_date_end = fields.Date(string='Contract End Date')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    emp.id AS id,
                    emp.id AS employee_id,
                    emp.name AS employee_name,
                    hc.id AS contract_id,
                    hc.state AS contract_state,
                    hc.date_end AS contract_date_end
                FROM hr_employee emp
                LEFT JOIN hr_contract hc ON hc.id = (
                    SELECT id FROM hr_contract
                    WHERE employee_id = emp.id AND date_end IS NOT NULL
                    ORDER BY date_end DESC
                    LIMIT 1
                )
                WHERE hc.id IS NOT NULL 
            )
        """)


