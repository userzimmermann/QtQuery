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

__all__ = ['QTypes']

from moretools import cached

from .align import AlignmentBase


class QTypes(type):
    @property
    @cached
    def Alignment(_Q):
        class Alignment(AlignmentBase, _Q.QtCore.Qt.Alignment):
            Q = _Q
            FLAGS = AlignmentBase.FLAGS(Q)

        return Alignment
