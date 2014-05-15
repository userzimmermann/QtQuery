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

from six import text_type as unicode

from . import Q, QtCore
from .align import ALIGNMENT


class Base(object):
    def __init__(self, props):
        pass


class QString(Base):
    def __repr__(self):
        return '<%s %s>' % (type(self).__name__, repr(unicode(self)))


class QObject(Base):
    def id(self):
        return self.qclass.objectName(self) or hex(id(self))

    def setId(self, value):
        self.qclass.setObjectName(self, value)

    def __repr__(self):
        return '<%s id=%s>' % (type(self).__name__, repr(self.id))


class QWidget(QObject):
    def __init__(self, props):
        QObject.__init__(self, props)
        layout = props.pop('layout', None)
        children = props.pop('children', ())
        if layout:
            self.setLayout(layout)
            layout = self.qclass.layout(self)
            for rown, q in enumerate(children):
                try:
                    row = iter(q)
                except TypeError:
                    layout.addWidget(q)
                else:
                    for coln, q in enumerate(row):
                        layout.addWidget(q, rown, coln)
        else:
            for q in children:
                q.setParent(self)

    def __iter__(self):
        raise TypeError

    def setAlignment(self, qalign):
        if isinstance(qalign, str):
            flags = [ALIGNMENT[flag] for flag in qalign]
            qalign = flags[0]
            for flag in flags[1:]:
                qalign |= flag
        else:
            qalign = QtCore.Qt.Alignment(qalign)
        self.qclass.setAlignment(self, qalign)

    def setLayout(self, qlayout):
        if isinstance(qlayout, str):
            qlayout = getattr(Q, qlayout + 'Layout')()
        self.qclass.setLayout(self, qlayout)
