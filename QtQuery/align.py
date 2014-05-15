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

__all__ = ['ALIGNMENT', 'Alignment']

from . import QtCore


ALIGNMENT = {
  '<': QtCore.Qt.AlignLeft,
  '>': QtCore.Qt.AlignRight,
  '|': QtCore.Qt.AlignHCenter,
  '^': QtCore.Qt.AlignTop,
  '_': QtCore.Qt.AlignBottom,
  '-': QtCore.Qt.AlignVCenter,
  '+': QtCore.Qt.AlignCenter,
  }


class Alignment(QtCore.Qt.Alignment):
    def __init__(self, qalign):
        if isinstance(qalign, str):
            flags = [ALIGNMENT[flag] for flag in qalign]
            qalign = flags[0]
            for flag in flags[1:]:
                qalign |= flag
        QtCore.Qt.Alignment.__init__(self, qalign)
