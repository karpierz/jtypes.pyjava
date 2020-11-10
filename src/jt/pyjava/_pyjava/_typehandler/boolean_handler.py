# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public

from .._constants import EJavaType
from .._constants import EMatch
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler


@public
class BooleanHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):
        super().__init__(state, EJavaType.BOOLEAN,
                         JVM.jvm.JClass.getBooleanClass())

    def match(self, val):
        if isinstance(val, bool):
            return EMatch.PERFECT
        return EMatch.NONE

    def toJava(self, val):
        val = val is True
        return self._jt_jvm.JObject.newBoolean(val)

    def toPython(self, val):
        if isinstance(val, self._jt_jvm.JObject):
            return val.booleanValue()
        else:
            return bool(val)

    def getStatic(self, fld, cls):
        return fld.getStaticBoolean(cls)

    def setStatic(self, fld, cls, val):
        val = val is True
        fld.setStaticBoolean(cls, bool(val))

    def getInstance(self, fld, this):
        return fld.getBoolean(this)

    def setInstance(self, fld, this, val):
        val = val is True
        fld.setBoolean(this, bool(val))

    def setArgument(self, pdescr, args, pos, val):
        val = val is True
        args.setBoolean(pos, bool(val))

    """
    elif arg_definition == "C":

        args.setChar(pos, val)
    """

    def callStatic(self, meth, cls, args):
        return meth.callStaticBoolean(cls, args)

    def callInstance(self, meth, this, args):
        return meth.callInstanceBoolean(this, args)
