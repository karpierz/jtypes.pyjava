# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public
from jvm.lib import cached

from .._constants import EJavaType
from .._constants import EMatch
from .._jvm       import JVM

from ._base_handler import _ObjectHandler


@public
class StringHandler(_ObjectHandler):

    __slots__ = ()

    def __init__(self, state):
        super().__init__(state, EJavaType.STRING,
                         JVM.jvm.JClass.getStringClass())

    @cached
    def _class(self):
        return self._state.class_importer.java_lang_String

    def match(self, val):
        if val is None:
            return EMatch.IMPLICIT
        elif isinstance(val, str):
            return EMatch.PERFECT
        elif isinstance(val, self._class()):#and val.__javaobject__.getClass() == self._class():
            return EMatch.PERFECT
        return EMatch.NONE

    def toJava(self, val):
        if val is None:
            return None
        elif isinstance(val, str):
            return self._jt_jvm.JObject.newString(val)
        elif isinstance(val, self._class()):#and val.__javaobject__.getClass() == self._class():
            return val.__javaobject__
        raise TypeError("Cannot convert value to Java string")

    def toPython(self, val):
        if val is None:
            return None
        else:
            if isinstance(val, self._jt_jvm.JObject):
                val = val.stringValue()
            return val

    def getStatic(self, fld, cls):
        return fld.getStaticString(cls)

    def setStatic(self, fld, cls, val):
        if val is None:
            fld.setStaticString(cls, None)
        elif isinstance(val, str):
            fld.setStaticString(cls, val)
        elif isinstance(val, self._class()):
            fld.setStaticObject(cls, val.__javaobject__)
        else:
            raise TypeError("Cannot convert value to Java string")

    def getInstance(self, fld, this):
        return fld.getString(this)

    def setInstance(self, fld, this, val):
        if val is None:
            fld.setString(this, None)
        elif isinstance(val, str):
            fld.setString(this, val)
        elif isinstance(val, self._class()):
            fld.setObject(this, val.__javaobject__)
        else:
            raise TypeError("Cannot convert value to Java string")

    def setArgument(self, pdescr, args, pos, val):
        if val is None:
            args.setString(pos, None)
        elif isinstance(val, str):
            args.setString(pos, val)
        elif isinstance(val, self._class()):
            args.setObject(pos, val.__javaobject__)
        else:
            raise TypeError("Cannot convert value to Java string")

    def callStatic(self, meth, cls, args):
        value = meth.callStaticString(cls, args)
        return value

    def callInstance(self, meth, this, args):
        value = meth.callInstanceString(this, args)
        return value
