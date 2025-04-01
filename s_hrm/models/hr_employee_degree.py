from odoo import models, fields

class EmployeeDegree(models.Model):
    _name = "hr.employee.degree"
    _description = "Employee Degree"

    name = fields.Char(string="Degree Name", required=True)
    employee_id = fields.Many2one("hr.employee", string="Employee")
    major = fields.Char(string="Major")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    classification = fields.Char(string="Classification")
    certificate = fields.Char(string="Certificate")
