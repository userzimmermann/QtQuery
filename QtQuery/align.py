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

__all__ = ['AlignmentBase', 'Aligned']

from moretools import cached


class AlignmentBase(object):
    @staticmethod
    def FLAGS(Q):
        return {
          '<': Q.QtCore.Qt.AlignLeft,
          '>': Q.QtCore.Qt.AlignRight,
          '|': Q.QtCore.Qt.AlignHCenter,
          '^': Q.QtCore.Qt.AlignTop,
          '_': Q.QtCore.Qt.AlignBottom,
          '-': Q.QtCore.Qt.AlignVCenter,
          '+': Q.QtCore.Qt.AlignCenter,
          }

    def __init__(self, qalign):
        Q = self.Q
        if isinstance(qalign, str):
            flags = [self.FLAGS[flag] for flag in qalign]
            qalign = flags[0]
            for flag in flags[1:]:
                qalign |= flag
        Q.QtCore.Qt.Alignment.__init__(self, qalign)


class AlignedMeta(type):
    @cached
    def __getitem__(cls, _qalign):
        Q = cls.Q
        class Aligned(cls):
            qalign = Q.Alignment(_qalign)

            def __init__(self, q):
                self.q = cls.Q(q)

        Aligned.__module__ = cls.__module__
        Aligned.__name__ = '%s[%s]' % (cls.__name__, repr(_qalign))
        return Aligned

    def __getattr__(cls, name):
        Q = cls.Q
        class Proxy(object):
            def __init__(self, consumer, attr):
                self.consumer = consumer
                ## self.attr = getattr(Q, attrname)
                self.attr = attr

            def __getitem__(self, arg):
                return type(self)(self.consumer, self.attr[arg])

            def __call__(self, *args, **kwargs):
                q = self.attr(*args, **kwargs)
                return self.consumer(q)

        return Proxy(cls, getattr(Q, name))


class Aligned(with_metaclass(AlignedMeta, object)):
    def __init__(self, qalign, q):
        Q = self.Q
        self.qalign = Q.Alignment(qalign)
        self.q = Q(q)
