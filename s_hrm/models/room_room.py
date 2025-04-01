# -*- coding: utf-8 -*-
from odoo import api, fields, models


class RoomRoom(models.Model):
    _inherit = "room.room"

    def _compute_is_available(self):
        now = fields.Datetime.now()
        booked_rooms = {room.id for room, in self.env["room.booking"]._read_group(
            [("start_datetime", "<=", now), ("stop_datetime", ">=", now), ("room_id", "in", self.ids),('state','=','confirm')],
            ["room_id"],
        )}
        for room in self:
            room.is_available = room.id not in booked_rooms

    def _compute_bookings_count(self):
        bookings_count_by_room = dict(self.env["room.booking"]._read_group(
            [("stop_datetime", ">=", fields.Datetime.now()), ("room_id", "in", self.ids), ('state','=','confirm')],
            ["room_id"],
            ["__count"]
        ))
        for room in self:
            room.bookings_count = bookings_count_by_room.get(room, 0)
