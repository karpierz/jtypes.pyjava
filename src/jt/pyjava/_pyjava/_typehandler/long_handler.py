# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public

from .._constants import EJavaType
from .._constants import EMatch
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler


@public
class LongHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):
        super().__init__(state, EJavaType.LONG,
                         JVM.jvm.JClass.getLongClass())

    def match(self, val):
        if isinstance(val, int):
            return EMatch.PERFECT
        return EMatch.NONE

    def valid(self, val):
        if isinstance(val, int):
            min_val, max_val = self._jt_jvm.JObject.minmaxLongValue()
            if not (min_val <= val <= max_val):
                return False
        return True

    def toJava(self, val):
        val = int(val)
        return self._jt_jvm.JObject.newLong(val)

    def toPython(self, val):
        if isinstance(val, self._jt_jvm.JObject):
            return val.longValue()
        else:
            return val

    def getStatic(self, fld, cls):
        return fld.getStaticLong(cls)

    def setStatic(self, fld, cls, val):
        fld.setStaticLong(cls, int(val))

    def getInstance(self, fld, this):
        return fld.getLong(this)

    def setInstance(self, fld, this, val):
        fld.setLong(this, int(val))

    def setArgument(self, pdescr, args, pos, val):
        args.setLong(pos, int(val))

    def callStatic(self, meth, cls, args):
        return meth.callStaticLong(cls, args)

    def callInstance(self, meth, this, args):
        return meth.callInstanceLong(this, args)
