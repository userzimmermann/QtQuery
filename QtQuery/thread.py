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

__all__ = ['ThreadBase']

import sys
from types import MethodType

from decorator import decorator


class ThreadBase(object):
    def __init__(self, func=None):
        Q = self.Q
        Q.QtCore.QThread.__init__(self)
        if func:
            self.run(func)

    def run(self, func):
        self.run = MethodType(lambda self: func(), self)

    def __call__(self):
        return self.start()


class ThreadedDeco(object):
    def __init__(self, Q):
        self.Q = Q

    def __call__(self, func=None):
        Q = self.Q
        if not func:
            return self

        def caller(func, *args, **kwargs):
            for init in tfunc.initfuncs:
                init(*args, **kwargs)

            if tfunc.exitfuncs:
                exc = [None, None, None]

                def run():
                    try:
                        func(*args, **kwargs)
                    except:
                        exc[:] = sys.exc_info()
            else:
                def run():
                    func(*args, **kwargs)

            thread = Q.Thread(run)

            @thread.finished
            def _():
                tfunc.threads.remove(thread)
                if tfunc.exitfuncs:
                    for exit_ in tfunc.exitfuncs:
                        exit_(args[0], *exc)

            thread.start()
            tfunc.threads.append(thread)

        def init(func):
            tfunc.initfuncs.append(func)
            return func

        def exit(func):
            tfunc.exitfuncs.append(func)
            return func

        tfunc = decorator(caller, func)
        tfunc.init = init
        tfunc.exit = exit
        tfunc.initfuncs = []
        tfunc.exitfuncs = []
        tfunc.threads = []
        return tfunc
