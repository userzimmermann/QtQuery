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

__all__ = ['ID']


class ID(object):
    def __init__(self, Q):
        self.Q = Q

    def __getitem__(self, id):
        self.id = id
        return self

    def __call__(self, q):
        q = self.Q(q)
        q.id = self.id
        return q

    def __getattr__(self, name):
        class Proxy(object):
            def __init__(self, consumer, attr):
                self.consumer = consumer
                self.attr = attr

            def __getitem__(self, arg):
                return type(self)(self.consumer, self.attr[arg])

            def __getattr__(self, name):
                return type(self)(self.consumer, getattr(self.attr, name))

            def __call__(self, *args, **kwargs):
                q = self.attr(*args, **kwargs)
                return self.consumer(q)

        def consumer(q):
            q.id = self.id
            return q

        return Proxy(consumer, getattr(self.Q, name))
