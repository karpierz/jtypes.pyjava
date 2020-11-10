# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

import numbers

from jvm.lib import public

from .._constants import EJavaType
from .._constants import EMatch
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler
from ._base_handler import num_types


@public
class FloatHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):
        super().__init__(state, EJavaType.FLOAT,
                         JVM.jvm.JClass.getFloatClass())

    def match(self, val):
        if isinstance(val, numbers.Number):
            return EMatch.PERFECT
        return EMatch.NONE

    def valid(self, val):
        if isinstance(val, num_types):
            min_val, max_val = self._jt_jvm.JObject.minmaxFloatValue()
            if ((val > 0.0 and not ( min_val <= val <=  max_val)) or
                (val < 0.0 and not (-max_val <= val <= -min_val))):
                return False
        return True

    def toJava(self, val):
        val = float(val)
        return self._jt_jvm.JObject.newFloat(val)

    def toPython(self, val):
        if isinstance(val, self._jt_jvm.JObject):
            return val.floatValue()
        else:
            return val

    def getStatic(self, fld, cls):
        return fld.getStaticFloat(cls)

    def setStatic(self, fld, cls, val):
        fld.setStaticFloat(cls, float(val))

    def getInstance(self, fld, this):
        return fld.getFloat(this)

    def setInstance(self, fld, this, val):
        fld.setFloat(this, float(val))

    def setArgument(self, pdescr, args, pos, val):
        args.setFloat(pos, float(val))

    def callStatic(self, meth, cls, args):
        return meth.callStaticFloat(cls, args)

    def callInstance(self, meth, this, args):
        return meth.callInstanceFloat(this, args)
