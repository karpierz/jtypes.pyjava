# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public

from ._typehandler import *  # noqa


@public
class TypeManager:

    __slots__ = ('_state', '_handlers')

    def __init__(self, state=None):
        super().__init__()
        self._state    = state
        self._handlers = {}

    def start(self):
        self._register_handler(VoidHandler)
        self._register_handler(BooleanHandler)
        self._register_handler(CharHandler)
        self._register_handler(ByteHandler)
        self._register_handler(ShortHandler)
        self._register_handler(IntHandler)
        self._register_handler(LongHandler)
        self._register_handler(FloatHandler)
        self._register_handler(DoubleHandler)

    def stop(self):
        self._handlers = {}

    def _register_handler(self, hcls):
        thandler = hcls(self._state)
        self._handlers[thandler._jclass] = thandler
        return thandler

    def get_handler(self, jclass):
        thandler = self._handlers.get(jclass)
        if thandler is None:
            Handler = ArrayHandler if jclass.isArray() else ObjectHandler
            self._handlers[jclass] = thandler = Handler(self._state, jclass)
        return thandler
