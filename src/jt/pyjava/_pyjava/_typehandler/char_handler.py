# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public

from .._constants import EJavaType
from .._constants import EMatch
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler


@public
class CharHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):
        super().__init__(state, EJavaType.CHAR,
                         JVM.jvm.JClass.getCharClass())

    def match(self, val):
        if isinstance(val, str):
            if len(val) == 1:
                return EMatch.PERFECT
        return EMatch.NONE

    def valid(self, val):
        if isinstance(val, str):
            if len(val) != 1:
                return False
        return True

    def toJava(self, val):
        val = val[0]
        if isinstance(val, str):
            return self._jt_jvm.JObject.newCharacter(val)
        else: # isinstance(val, str)
            # Hmm, this is supposed to be UCS2...
            # but Java provides only 16 bits as well...
            return self._jt_jvm.JObject.newCharacter(val)

    def toPython(self, val):
        if isinstance(val, self._jt_jvm.JObject):
            return val.charValue()
        else:
            return val

    def getStatic(self, fld, cls):
        return fld.getStaticChar(cls)

    def setStatic(self, fld, cls, val):
        val = val[0]
        if isinstance(val, str):
            fld.setStaticChar(cls, val)
        else: # isinstance(val, str)
            # Hmm, this is supposed to be UCS2...
            # but Java provides only 16 bits as well...
            fld.setStaticChar(cls, val)

    def getInstance(self, fld, this):
        return fld.getChar(this)

    def setInstance(self, fld, this, val):
        val = val[0]
        if isinstance(val, str):
            fld.setChar(this, val)
        else: # isinstance(val, str)
            # Hmm, this is supposed to be UCS2...
            # but Java provides only 16 bits as well...
            fld.setChar(this, val)

    def setArgument(self, pdescr, args, pos, val):
        val = val[0]
        if isinstance(val, str):
            args.setChar(pos, val)
        else: # isinstance(val, str)
            # Hmm, this is supposed to be UCS2...
            # but Java provides only 16 bits as well...
            args.setChar(pos, val)

    def callStatic(self, meth, cls, args):
        return meth.callStaticChar(cls, args)

    def callInstance(self, meth, this, args):
        return meth.callInstanceChar(this, args)
