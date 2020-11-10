# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public

from .._constants import EJavaType
from .._constants import EMatch
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler


@public
class IntHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):
        super().__init__(state, EJavaType.INT,
                         JVM.jvm.JClass.getIntClass())

    def match(self, val):
        if isinstance(val, int):
            return EMatch.PERFECT
        return EMatch.NONE

    def valid(self, val):
        if isinstance(val, int):
            min_val, max_val = self._jt_jvm.JObject.minmaxIntValue()
            if not (min_val <= val <= max_val):
                return False
        return True

    def toJava(self, val):
        val = int(val)
        return self._jt_jvm.JObject.newInteger(val)

    def toPython(self, val):
        if isinstance(val, self._jt_jvm.JObject):
            return val.intValue()
        else:
            return val

    def getStatic(self, fld, cls):
        return fld.getStaticInt(cls)

    def setStatic(self, fld, cls, val):
        fld.setStaticInt(cls, int(val))

    def getInstance(self, fld, this):
        return fld.getInt(this)

    def setInstance(self, fld, this, val):
        fld.setInt(this, int(val))

    def setArgument(self, pdescr, args, pos, val):
        args.setInt(pos, int(val))

    def callStatic(self, meth, cls, args):
        return meth.callStaticInt(cls, args)

    def callInstance(self, meth, this, args):
        return meth.callInstanceInt(this, args)
