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

from .align import Aligned
from .label import Labeled
from .disable import Disabled
from .dock import Dockable


class Base(object):
    def __init__(self, props):
        pass


class QString(Base):
    def __repr__(self):
        return '<%s %s>' % (type(self).__name__, repr(unicode(self)))


class QSize(Base):
    def __iter__(self):
        yield self.qclass.width(self)
        yield self.qclass.height(self)

    def __div__(self, factor):
        Q = self.Q
        return Q(self.qclass.__div__(self, factor))

    def __getitem__(self, index):
        if index == 0:
            return self.qclass.width(self)
        if index == 1:
            return self.qclass.height(self)
        raise IndexError(index)


class QPalette(Base):
    @property
    def background(self):
        Q = self.Q
        return Q(self.qclass.background(self))


class QObject(Base):
    def id(self):
        return self.qclass.objectName(self) or hex(id(self))

    def setId(self, value):
        self.qclass.setObjectName(self, value)

    def shortcut(self, key, func=None):
        Q = self.Q
        def shortcut(func):
            return Q.Shortcut(key, self.q, func)

        if func:
            return shortcut(func)
        return shortcut

    def __repr__(self):
        return '<%s id=%s>' % (type(self).__name__, repr(self.id))


class QWidget(QObject):
    def __init__(self, props):
        Q = self.Q
        QObject.__init__(self, props)
        layout = props.pop('layout', None)
        children = props.pop('children', ())
        if layout:
            self.setLayout(layout)
            layout = self.qclass.layout(self)
            for rown, q in enumerate(children):
                if isinstance(q, str):
                    q = Q.Label(text=q)
                    layout.addWidget(q)
                    continue
                try:
                    row = iter(q)
                except TypeError:
                    if isinstance(q, Aligned):
                        layout.addWidget(q.q, 0, q.qalign)
                    elif isinstance(q, Labeled):
                        qlayout = {'<': 'HBox', '^': 'VBox'}[q.qpos]
                        qpanel = Q.Widget(layout=qlayout, children=[
                          q.qlabel, q.q
                          ])
                        layout.addWidget(qpanel)
                    else:
                        layout.addWidget(q)
                else:
                    for coln, q in enumerate(row):
                        if isinstance(q, str):
                            q = Q.Label(text=q)
                            layout.addWidget(q, rown, coln)
                        elif isinstance(q, Aligned):
                            layout.addWidget(q.q, rown, coln, q.qalign)
                        else:
                            layout.addWidget(q, rown, coln)
        else:
            for q in children:
                q.setParent(self)

    def __iter__(self):
        raise TypeError

    def setId(self, value):
        QObject.setId(self, value)
        try:
            dock = self.dock
        except AttributeError:
            return
        dock.setId(value + '.dock')

    @property
    def size(self):
        Q = self.Q
        return Q(self.qclass.size(self))

    @property
    def width(self):
        return self.qclass.width(self)

    @property
    def height(self):
        return self.qclass.height(self)

    def setAlignment(self, qalign):
        Q = self.Q
        qalign = Q.Alignment(qalign)
        self.qclass.setAlignment(self, qalign)

    def setLayout(self, qlayout):
        Q = self.Q
        if isinstance(qlayout, str):
            qlayout = getattr(Q, qlayout + 'Layout')()
        self.qclass.setLayout(self, qlayout)

    def disabled(self):
        return Disabled(q=self)


class QMainWindow(QWidget):
    @property
    def dockable(self):
        Q = self.Q
        return Dockable(Q, qwindow=self)

