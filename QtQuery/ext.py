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

from . import Q


class Base(object):
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
    def setLayout(self, qlayout):
        if isinstance(qlayout, str):
            qlayout = getattr(Q, qlayout + 'Layout')()
        self.qclass.setLayout(self, qlayout)
