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


@public
class VoidHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):

        super(VoidHandler, self).__init__(state, EJavaType.VOID,
                                          JVM.jvm.JClass.getVoidClass())
    def match(self, val):

        return EMatchType.NONE

    def valid(self, val):

        return True

    def toJava(self, val):

        return None

    def toPython(self, val):

        return None

    def getStatic(self, fld, cls):

        raise RuntimeError("void cannot be the type of a static field.")

    def setStatic(self, fld, cls, val):

        raise RuntimeError("void cannot be the type of a static field.")

    def getInstance(self, fld, this):

        raise RuntimeError("void cannot be the type of a field.")

    def setInstance(self, fld, this, val):

        raise RuntimeError("void cannot be the type of a field.")

    def setArgument(self, pdescr, args, pos, val):

        raise RuntimeError("void cannot be the type of an arument.")

    def callStatic(self, meth, cls, args):

        return meth.callStaticVoid(cls, args)

    def callInstance(self, meth, this, args):

        return meth.callInstanceVoid(this, args)
