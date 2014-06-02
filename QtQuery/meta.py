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

__all__ = ['QMeta']

from inspect import isclass
from itertools import chain
from functools import partial

from moretools import cached, camelize

from .tools import QTools
from .event import Event
from .signal import Signal
from .emit import Emitter
from . import ext


class QMeta(QTools):

    def import_(Q, *modnames):
        mods = [getattr(__import__(Q.qmodule.__name__ + '.' + name), name)
                for name in modnames]
        for name, mod in zip(modnames, mods):
            Q.qsubmodules.append(mod)
            setattr(type(Q), name, mod)

    @cached
    def qclass(Q, name):
        if not name.startswith('Q'):
            name = 'Q' + name
        for mod in Q.qsubmodules:
            try:
                return getattr(mod, name)
            except AttributeError:
                pass
        raise ValueError(name)

    def __instancecheck__(Q, obj):
        return isinstance(obj, Q.QtCore.QObject) and hasattr(obj, 'qclass')

    @cached
    def __getitem__(_Q, _qclass):
        if isclass(_qclass):
            if not (issubclass(_qclass, _Q.QtCore.QObject)
                    or _qclass.__module__.startswith(_Q.qmodule.__name__)
                    ):
                raise TypeError(_qclass)
        else:
            _qclass = _Q.qclass(_qclass)

        for qclass in _qclass.mro():
            try:
                _qxclass = getattr(ext, qclass.__name__)
                break
            except AttributeError:
                pass
        else:
            _qxclass = ext.Base

        class Q_(_qxclass, _qclass):
            Q = _Q
            qclass = _qclass
            qxclass = _qxclass

            signal = Q.qsignalclass(partial)

            def __new__(cls, *args, **kwargs):
                return cls.qclass.__new__(cls)

            def __init__(self, *args, **kwargs):
                Q = self.Q
                if args and args[0] is self:
                    return

                self.qclass.__init__(self, *args)
                self.q = self
                self.qxclass.__init__(self, kwargs)
                for name, value in kwargs.items():
                    if name == "id":
                        self.id = value
                        continue
                    try:
                        setter = object.__getattribute__(
                          self, 'set' + camelize(name))
                    except AttributeError:
                        attr = object.__getattribute__(self, name)
                        if name.endswith('Event'):
                            try:
                                event = self.__dict__[name]
                            except KeyError:
                                event = self.__dict__[name] = Event(name, attr)
                            if callable(value):
                                event.slots = [value]
                            else:
                                event.slots = value
                        elif isinstance(attr, Q.qboundsignalclass):
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
                    else:
                        setter(value)

                @self.signal
                def slot(partial):
                    partial()

                self.emit = Emitter(q=self)

            def __getattribute__(self, name):
                Q = type(self).Q
                if name == 'Q':
                    return Q
                try:
                    object.__getattribute__(self, 'set' + camelize(name))
                except AttributeError:
                    attr = object.__getattribute__(self, name)
                    if name.endswith('Event'):
                        try:
                            event = self.__dict__[name]
                        except KeyError:
                            event = self.__dict__[name] = Event(name, attr)
                        return event
                    if isinstance(attr, Q.qboundsignalclass):
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
                if isinstance(value, (Q.QtCore.QObject, Q.qbaseclass)):
                    return Q(value)
                return value

            def __setattr__(self, name, value):
                Q = type(self).Q
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
                    if isinstance(attr, Q.qboundsignalclass):
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

            def __call__(self, qclass=None, **filters):
                Q = type(self).Q
                qlist = []
                if not qclass:
                    qclass = Q.QtCore.QObject
                elif isinstance(qclass, str):
                    qclass = Q.qclass(qclass)
                elif isinstance(qclass, Q):
                    qclass = qclass.qclass

                def find(q):
                    for q in q.children():
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

            def __getitem__(self, id):
                qlist = self(id=id)
                if not qlist:
                    raise KeyError(id)
                if len(qlist) > 1:
                    raise RuntimeError(
                      "More than 1 widgets with id '%s'." % id)
                return qlist[0]

        Q_.__name__ = 'Q[%s]' % (_qclass.__name__)
        return Q_

    def __getattr__(Q, name):
        return Q[name]

    def _getAttributeNames(Q):
        return [name[1:] for name in chain(*map(dir, Q.qsubmodules))
                if name[0] == 'Q']
