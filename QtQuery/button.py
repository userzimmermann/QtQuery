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

__all__ = ['ButtonDeco']


from . import Q


class ButtonDeco(object):
    def __init__(self):
        self.id = None
        self.text = None

    def __call__(self, func=None, id=None, text=None):
        if not func:
            if id:
                self.id = id
            if text:
                self.text = text
            return self

        props = {}
        id = id or self.id
        if id:
            props['id'] = id
        props['text'] = text or self.text or func.__name__.capitalize()

        def button(*args):
            q = Q.PushButton(**props)
            q.clicked += lambda: func(*args)
            return q

        func.button = button
        return func
