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

from moretools import camelize


class ButtonDeco(object):
    def __init__(self, Q):
        self.Q = Q
        self.id = None
        self.text = None

    def __call__(self, func=None, id=None, text=None):
        if not func:
            if id:
                self.id = id
            if text:
                self.text = text
            return self

        props = {
          'text': text or self.text or camelize(func.__name__, joiner=' '),
          'clicked': lambda arg: func(),
          }
        id = id or self.id
        if id:
            if id is True:
                id = func.__name__ + 'Button'
            props['id'] = id
        return self.Q.PushButton(**props)
