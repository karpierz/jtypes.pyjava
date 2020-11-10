# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public
from jvm.jtypehandlerabc import TypeHandlerABC

num_types  = (float, int)
byte_types = (bytes, bytearray)


class _BaseHandler(TypeHandlerABC):

    __slots__ = ('_jt_jvm',)

    def __init__(self, state, jtype, jclass):
        super().__init__(state, jtype, jclass)
        self._jt_jvm = self._jclass.jvm

    def isSubtypeOf(self, other):
        raise NotImplementedError()

    def newArray(self, size):
        raise NotImplementedError()

    def getElement(self, arr, idx):
        raise NotImplementedError()

    def setElement(self, arr, idx, val):
        raise NotImplementedError()

    def getSlice(self, arr, start, stop, step):
        raise NotImplementedError()

    def setSlice(self, arr, start, stop, step, val):
        raise NotImplementedError()

    def getArrayBuffer(self, arr):
        raise NotImplementedError()

    def releaseArrayBuffer(self, arr, buf):
        raise NotImplementedError()


class _PrimitiveHandler(_BaseHandler):

    __slots__ = ()

    def valid(self, val):
        return True


class _ObjectHandler(_BaseHandler):

    __slots__ = ()

    def valid(self, val):
        return True

    def getStatic(self, fld, cls):
        jobject = fld.getStaticObject(cls)
        return self.toPython(jobject)

    def setStatic(self, fld, cls, val):
        fld.setStaticObject(cls, self.toJava(val))

    def getInstance(self, fld, this):
        jobject = fld.getObject(this)
        return self.toPython(jobject)

    def setInstance(self, fld, this, val):
        fld.setObject(this, self.toJava(val))

    def setArgument(self, pdescr, args, pos, val):
        args.setObject(pos, self.toJava(val))

    def callStatic(self, meth, cls, args):
        jobject = meth.callStaticObject(cls, args)
        return self.toPython(jobject)

    def callInstance(self, meth, this, args):
        jobject = meth.callInstanceObject(this, args)
        return self.toPython(jobject)
