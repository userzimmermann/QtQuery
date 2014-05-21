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

__all__ = ['QBase']

from moretools import camelize

from .meta import QMeta


class QBase(with_metaclass(QMeta, object)):
    def __new__(Q, qobjects):
        if isinstance(qobjects, Q):
            return qobjects

        if isinstance(qobjects, (Q.QtCore.QObject, Q.qbaseclass)):
            qobjects.__class__ = Q[qobjects.__class__]
            return qobjects

        return object.__new__(Q)

    def __init__(self, qobjects):
        ## self.Q = Q = type(self)
        Q = self.Q
        self.qlist = []
        for q in qobjects:
            if not isinstance(q, (Q.QtCore.QObject, Q.qbaseclass)):
                raise TypeError(type(q))
            self.qlist.append(Q(q))

    def __getitem__(self, index):
        return self.qlist[index]

    ## __getattribute__ = object.__getattribute__

    def __getattr__(self, name):
        Q = self.Q
        values = []
        for q in self.qlist:
            obj = object.__getattribute__(q, name)
            if hasattr(q, 'set' + camelize(name)):
                values.append(obj())
            else:
                values.append(obj)
        try:
            return Q(values)
        except TypeError:
            return tuple(values)

    def __setattr__(self, name, value):
        if name == 'qlist':
            object.__setattr__(self, name, value)
        for q in self.qlist:
            try:
                setter = getattr(q, 'set' + camelize(name))
            except AttributeError:
                object.__setattr__(self, name, value)
                break
            else:
                setter(value)

    def __dir__(self):
        if not self.qlist:
            return []
        names = set(dir(self.qlist[0]))
        for q in self.qlist[1:]:
            names.intersection_update(dir(q))
        return names

    def __repr__(self):
        return 'Q(%s)' % repr(self.qlist)
