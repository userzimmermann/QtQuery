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

from .types import QTypes
from .qid import ID
from .align import Aligned as _Aligned
from .label import Labeled as _Labeled
from .button import ButtonDeco


class QTools(QTypes):

    @property
    def id(Q):
        return ID(Q)

    def label(Q, qlabel):
        if isinstance(qlabel, Q.Label.qclass):
            qlabel = qlabel.text
        return Q.Label(text=qlabel)

    def panel(Q, children=None):
        return Q.Widget(children=children)

    def hbox(Q, children=None):
        return Q.Widget(layout='HBox', children=children)

    def vbox(Q, children=None):
        return Q.Widget(layout='VBox', children=children)

    def grid(Q, children=None):
        return Q.Widget(layout='Grid', children=children)

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
