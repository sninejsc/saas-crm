# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RoomBooking(models.Model):
    _name = 'room.booking'
    _inherit = ['room.booking', 'mail.thread', 'mail.activity.mixin', 'tier.validation']

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('confirm', 'Confirm'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', tracking=True)

    _state_field = "state"
    _state_from = ['draft', 'in_progress']
    _state_to = ['confirm']
    _to_approve_state = 'in_progress'
    _approved_state = 'confirm'
    _rejected_state = 'rejected'
    _subject_prefix = '[Room Management System]'
    _subject_code = 'to_employee_id'
    _enable_restart_validation = False
    _tier_validation_manual_config = False

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def action_to_draft(self):
        for record in self:
            record.state = 'draft'

    def _check_unique_slot(self):
        pass

    def _check_state(self):
        min_start = self.start_datetime
        max_stop = self.stop_datetime

        bookings_by_room = self.search([
            ("room_id", "=", self.room_id.id),
            ("start_datetime", "<", max_stop),
            ("stop_datetime", ">", min_start),
            ("state", "=", "confirm"),
        ])

        if bookings_by_room.filtered(
                lambda b: b.id != self.id and b.start_datetime < max_stop and b.stop_datetime > min_start
        ):
            raise ValidationError(_(
                "Room %s is already booked during the selected time slot.") % self.room_id.name)

    def validate_tier(self):
        self._check_state()
        return super(RoomBooking, self).validate_tier()
