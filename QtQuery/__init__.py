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

from inspect import ismodule

from moretools import simpledict

from .base import QBase


def Q(_qmodule):
    """Create a Q for the given Python Qt implementation name
       or module instance.
    """
    if not ismodule(_qmodule):
        _qmodule = __import__(str(_qmodule))

    class QMeta(type(QBase)):
        qmodule = _qmodule
        # Holds all the Qt... sub module instances imported with Q.import_():
        qsubmodules = []

    class Q(with_metaclass(QMeta, QBase)):
        pass

    Q.Q = Q

    Q.import_('QtCore', 'QtGui')
    try: # Qt 5.x implementations
        Q.import_('QtWidgets')
    except ImportError:
        pass
    #HACK: Get the base C++ wrapper class of the given Qt implementation:
    QMeta.qbaseclass = Q.QtCore.QObject.mro()[-2]
    #HACK: Get the class of bound signal instances:
    QMeta.qsignalclass = type(Q.QtCore.QObject().destroyed)

    return Q
