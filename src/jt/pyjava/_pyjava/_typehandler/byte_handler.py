# Copyright (c) 2015-2019 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from ....jvm.lib.compat import *
from ....jvm.lib import annotate
from ....jvm.lib import public

from .._constants import EJavaType
from .._constants import EMatchType
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler
from ._base_handler import int_types, byte_types


@public
class ByteHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):

        super(ByteHandler, self).__init__(state, EJavaType.BYTE,
                                          JVM.jvm.JClass.getByteClass())
    def match(self, val):

        if isinstance(val, int_types):
            return EMatchType.PERFECT
        return EMatchType.NONE

    def valid(self, val):

        if isinstance(val, int_types):
            min_val, max_val = self._jt_jvm.JObject.minmaxByteValue()
            if not (min_val <= val <= max_val):
                return False
        return True

    def toJava(self, val):

        val = int(val)
        return self._jt_jvm.JObject.newByte(val)

    def toPython(self, val):

        if isinstance(val, self._jt_jvm.JObject):
            return val.byteValue()
        else:
            return val

    def getStatic(self, fld, cls):

        return fld.getStaticByte(cls)

    def setStatic(self, fld, cls, val):

        #if isinstance(val, byte_types):
        #    fld.setStaticByte(cls, byte(val[0]))
        #else:
        fld.setStaticByte(cls, int(val))

    def getInstance(self, fld, this):

        return fld.getByte(this)

    def setInstance(self, fld, this, val):

        #if isinstance(val, byte_types):
        #    fld.setByte(this, byte(val[0]))
        #else:
        fld.setByte(this, int(val))

    def setArgument(self, pdescr, args, pos, val):

        #if isinstance(val, byte_types):
        #    args.setByte(pos, byte(val[0]))
        #else:
        args.setByte(pos, int(val))

    def callStatic(self, meth, cls, args):

        return meth.callStaticByte(cls, args)

    def callInstance(self, meth, this, args):

        return meth.callInstanceByte(this, args)
