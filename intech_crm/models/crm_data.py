# -*- coding: utf-8 -*-

from odoo import fields, models, api


class CrmData(models.Model):
    _name = 'crm.data'
    _description = 'CRM Data'
    _sql_constraints = [
        ('name_uniq', 'unique (name, type)', "Name and Type already exists !"),
    ]

    name = fields.Char(string='Name')
    type = fields.Selection(string='Type',
                            selection=[('group', 'Group Partner'),
                                       ('source', 'Source Partner'),
                                       ('relation', 'Relation')],
                            required=True)
