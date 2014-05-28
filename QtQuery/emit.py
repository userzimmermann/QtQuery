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

from functools import partial


class Emitter(object):
    def __init__(self, q, signal=None):
        object.__setattr__(self, 'q', q)
        object.__setattr__(self, 'signal', signal or q.signal)

    def __call__(self, signal, *args):
        self.q.qclass.emit(self, signal, *args)

    def __getattr__(self, name):
        def emitter(*args, **kwargs):
            def caller(*args, **kwargs):
                getattr(self.q, name)(*args, **kwargs)

            self.signal.emit(partial(caller, *args, **kwargs))

        return emitter

    def __setattr__(self, name, value):
        self.signal.emit(partial(setattr, self.q, name, value))
