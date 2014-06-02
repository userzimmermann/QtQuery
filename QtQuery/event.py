# QtQuery
#
# A jQuery inspired Pythonic Qt experience.
#
# Copyright (C) 2014 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# QtQuery is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# QtQuery is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with QtQuery. If not, see <http://www.gnu.org/licenses/>.

__all__ = ['Event']


class Event(object):
    def __init__(self, name, qevent):
        self.name = name
        self._slots = []
        self.qevent = qevent

    @property
    def slots(self):
        return self._slots

    @slots.setter
    def slots(self, slots):
        self._slots = list(slots)

    def __add__(self, slots):
        if callable(slots):
            self._slots.append(slots)
        else:
            self._slots.extend(slots)
        return self

    def __sub__(self, slots):
        if callable(slots):
            self._slots.remove(slots)
        else:
            for slot in slots:
                self._slots.remove(slot)

    def __call__(self, slot):
        if callable(slot):
            self._slots.append(slot)
            return slot

        event = slot
        for slot in self._slots:
            slot(event)
        self.qevent(event)
