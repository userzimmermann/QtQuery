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

__all__ = ['Q']

from moretools import camelize, cached

import sip
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    try:
        from PyQt4 import QtCore, QtGui as QtWidgets
    except ImportError:
        from PySide import QtCore, QtGui as QtWidgets

from . import ext
from .signal import Signal


QObject = QtCore.QObject
QType = type(QtCore.QObject)

QSignal = QtCore.pyqtBoundSignal


class QMeta(type):

    def __instancecheck__(cls, obj):
        return isinstance(obj, QObject) and hasattr(obj, 'qclass')

    @cached
    def __getitem__(cls, _qclass):
        for qclass in _qclass.mro():
            try:
                _qext = getattr(ext, qclass.__name__)
                break
            except AttributeError:
                pass
        else:
            _qext = ext.Base

        class Q_(_qext, _qclass):
            qclass = _qclass
            qext = _qext

            def __new__(cls, _=None, **kwargs):
                return cls.qclass.__new__(cls)

            def __init__(self, *args, **kwargs):
                if args and args[0] is self:
                    return

                self.qclass.__init__(self, *args)
                self.q = self
                for name, value in kwargs.items():
                    if name == "id":
                        self.id = value
                        continue
                    try:
                        setter = object.__getattribute__(
                          self, 'set' + camelize(name))
                    except AttributeError:
                        signal = object.__getattribute__(self, name)
                        for func in value:
                            signal.connect(func)
                    else:
                        setter(value)

            def __getattribute__(self, name):
                try:
                    object.__getattribute__(self, 'set' + camelize(name))
                except AttributeError:
                    attr = object.__getattribute__(self, name)
                    if isinstance(attr, QSignal):
                        try:
                            signal = self.__dict__[name]
                        except KeyError:
                            signal = self.__dict__[name] = Signal(
                              name, attr)
                            attr.connect(signal.run)
                        return signal
                    return attr
                try:
                    getter = object.__getattribute__(self, name)
                except AttributeError:
                    getter = object.__getattribute__(
                      self, 'is' + camelize(name))
                value = getter()
                if isinstance(value, (QObject, sip.simplewrapper)):
                    return Q(value)
                return value


            def __setattr__(self, name, value):
                try:
                    setter = getattr(self, 'set' + camelize(name))
                except AttributeError:
                    pass
                else:
                    setter(value)
                    return

                try:
                    attr = object.__getattribute__(self, name)
                except AttributeError:
                    pass
                else:
                    if isinstance(attr, QSignal):
                        try:
                            signal = self.__dict__[name]
                        except KeyError:
                            signal = self.__dict__[name] = Signal(
                              name, attr)
                            attr.connect(signal.run)
                        if value is not signal:
                            if callable(value):
                                signal.slots = [value]
                            else:
                                signal.slots = value
                        return

                object.__setattr__(self, name, value)

            def __call__(self, qclass, **filters):
                qlist = []
                if isinstance(qclass, str):
                    qclass = getattr(QtWidgets, 'Q' + qclass)
                elif isinstance(qclass, Q):
                    qclass = qclass.qclass

                def find(q):
                    for q in q.children():
                        print(q)
                        if isinstance(q, qclass):
                            for name, query in filters.items():
                                try:
                                    value = getattr(q, name)
                                except AttributeError:
                                    break
                                if query != value:
                                    break
                            else:
                                qlist.append(q)
                        find(q)

                find(self)
                return Q(qlist)

        Q_.__name__ = 'Q[%s]' % (_qclass.__name__)
        return Q_

    def __getattr__(cls, name):
        qclass = getattr(QtWidgets, 'Q' + name)
        return cls[qclass]

    def _getAttributeNames(self):
        return [name[1:] for name in dir(QtGui) if name[0] == 'Q']


class Q(with_metaclass(QMeta, object)):
    def __new__(cls, qobjects):
        if isinstance(qobjects, Q):
            return qobjects

        if isinstance(qobjects, (QObject, sip.simplewrapper)):
            qobjects.__class__ = cls[qobjects.__class__]
            return qobjects

        return object.__new__(cls)

    def __init__(self, qobjects):
        self.qlist = []
        for q in qobjects:
            if not isinstance(q, (QObject, sip.simplewrapper)):
                raise TypeError(type(q))
            self.qlist.append(Q(q))

    def __getitem__(self, index):
        return self.qlist[index]

    ## __getattribute__ = object.__getattribute__

    def __getattr__(self, name):
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
