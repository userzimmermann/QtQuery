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

__all__ = ['QTools']


from moretools import cached

from .qtypes import QTypes
from .qid import ID
from .align import Aligned as _Aligned
from .label import Labeled as _Labeled
from .button import ButtonDeco
from .thread import ThreadedDeco
from .log import logger


class QTools(QTypes):

    @property
    def threaded(Q):
        return ThreadedDeco(Q)

    @property
    def id(Q):
        return ID(Q)

    def label(Q, qlabel, **props):
        if isinstance(qlabel, Q.Label.qclass):
            qlabel = qlabel.text
        return Q.Label(text=qlabel, **props)

    def panel(Q, children=None, **props):
        return Q.Widget(children=children, **props)

    def hbox(Q, children=None, **props):
        return Q.Widget(layout='HBox', children=children, **props)

    def vbox(Q, children=None, **props):
        return Q.Widget(layout='VBox', children=children, **props)

    def grid(Q, children=None, **props):
        return Q.Widget(layout='Grid', children=children, **props)

    @property
    @cached
    def aligned(_Q):
        class Aligned(_Aligned):
            Q = _Q

        return Aligned

    @property
    @cached
    def labeled(_Q):
        class Labeled(_Labeled):
            Q = _Q

        return Labeled

    @property
    def button(Q):
        return ButtonDeco(Q)

    @property
    def logger(Q):
        return logger(Q)
