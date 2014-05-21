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

from six import with_metaclass

__all__ = ['Labeled']

from moretools import cached


class LabeledMeta(type):
    @cached
    def __getitem__(cls, _qpos):
        Q = cls.Q
        class Labeled(cls):
            qpos = _qpos

            def __init__(self, qlabel, q=None):
                self.qlabel = Q.label(qlabel)
                ## self.q = q and cls.Q(q)
                self.q = q

        return Labeled


class Labeled(with_metaclass(LabeledMeta, object)):
    def __init__(self, qpos, qlabel, q=None):
        Q = self.Q
        self.qpos = qpos
        self.qlabel = Q.label(qlabel)
        self.q = q and Q(q)

    def __getattr__(self, name):
        Q = self.Q
        class Proxy(object):
            def __init__(self, consumer, attr):
                self.consumer = consumer
                self.attr = attr
                ## self.attr = getattr(Q, attr)

            def __getitem__(self, arg):
                return type(self)(self.consumer, self.attr[arg])

            def __call__(self, *args, **kwargs):
                q = self.attr(*args, **kwargs)
                return self.consumer(q)

        def consumer(q):
            return type(self)(self.qlabel, q)

        return Proxy(consumer, getattr(Q, name))
