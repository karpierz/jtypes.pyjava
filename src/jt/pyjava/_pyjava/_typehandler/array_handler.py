# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public
from jvm.lib import cached

from jvm.jstring import JString

from .._constants import EJavaType
from .._constants import EMatch
from .._jvm       import JVM
from .._util      import from_utf8

from ._base_handler import _ObjectHandler


@public
class ArrayHandler(_ObjectHandler):

    __slots__ = ('_component_thandler',)

    def __init__(self, state, jclass):
        super().__init__(state, EJavaType.ARRAY, jclass)
        self._component_thandler = None # state.type_manager.get_handler(jclass.getComponentType())

    @cached
    def _class(self):
        return self._state.array_importer.defineClass(self._jclass)

    componentHandler = property(lambda self: self._component_thandler)

    def match(self, val):
        if val is None:
            return EMatch.PERFECT
        else:
            # Checks that val is a JavaInstance and unwraps the jclass
            from .._javawrapper import unwrap_instance
            jobject, jclass = unwrap_instance(val, with_javaclass=True)
            if jobject is not None:
                # Check that the passed object has a class that is subclass of the wanted class
                if self._jclass.isAssignableFrom(jclass):
                    return EMatch.PERFECT
            else:
                # Special case: We can convert a unicode object to String
                jt_jvm = self._jt_jvm
                if (isinstance(val, str) and
                    self._jclass == jt_jvm.JClass(None, jt_jvm._jvm.String.Class, own=False)):
                    return EMatch.PERFECT
        return EMatch.NONE

    def toJava(self, val):
        if val is None:
            return None
        else:
            from .._javawrapper import unwrap_instance
            jobject, _ = unwrap_instance(val)
            if jobject is not None:
                return jobject
            else:
                # Special case: String objects can be created from unicode, which
                # makes sense. They can get converted back when received from Java.
                return from_utf8(val.encode("utf-8"))

    def toPython(self, val):
        if val is None:
            return None
        else:
            aval = val.asArray(self._component_thandler.javaType)
            if IF_OLD:
                jclass = aval.getClass()
                pclass = self._state.array_importer.defineClass(jclass)
            else:
                pclass = self._class()
            return pclass(aval)

    def getStatic(self, fld, cls):
        jobject = fld.getStaticObject(cls)
        if jobject is None:
            return None
        jt_jvm = self._jt_jvm
        if jobject.getClass() == jt_jvm.JClass(None, jt_jvm._jvm.String.Class, own=False):
            # Special case: String objects get converted to unicode,
            # which makes sense. They can get converted back if need be.
            with jt_jvm as (jvm, jenv):
                return JString(jenv, jobject.handle, own=False).str
        else:
            from .._javawrapper import wrap_instance
            return wrap_instance(jobject)

    def setStatic(self, fld, cls, val):
        if val is None:
            fld.setStaticObject(cls, None)
        else:
            from .._javawrapper import unwrap_instance
            jobject, _ = unwrap_instance(val)
            if jobject is not None:
                fld.setStaticObject(cls, jobject)
            else:
                # Special case: String objects can be created from unicode, which
                # makes sense. They can get converted back when received from Java.
                fld.setStaticString(cls, val.encode("utf-8").decode("utf-8"))

    def getInstance(self, fld, this):
        jobject = fld.getObject(this)
        if jobject is None:
            return None
        jt_jvm = self._jt_jvm
        if jobject.getClass() == jt_jvm.JClass(None, jt_jvm._jvm.String.Class, own=False):
            # Special case: String objects get converted to unicode,
            # which makes sense. They can get converted back if need be.
            with jt_jvm as (jvm, jenv):
                return JString(jenv, jobject.handle, own=False).str
        else:
            from .._javawrapper import wrap_instance
            return wrap_instance(jobject)

    def setInstance(self, fld, this, val):
        if val is None:
            fld.setObject(this, None)
        else:
            from .._javawrapper import unwrap_instance
            jobject, _ = unwrap_instance(val)
            if jobject is not None:
                fld.setObject(this, jobject)
            else:
                # Special case: String objects can be created from unicode, which
                # makes sense. They can get converted back when received from Java.
                fld.setString(this, val.encode("utf-8").decode("utf-8"))

    def setArgument(self, pdescr, args, pos, val):
        if val is None:
            args.setObject(pos, None)
        else:
            from .._javawrapper import unwrap_instance
            jobject, _ = unwrap_instance(val)
            if jobject is not None:
                args.setObject(pos, jobject)
            else:
                # Special case: String objects can be created from unicode, which
                # makes sense. They can get converted back when received from Java.
                args.setString(pos, val.encode("utf-8").decode("utf-8"))

    def callStatic(self, meth, cls, args):
        jobject = meth.callStaticObject(cls, args)
        if jobject is None:
            return None
        jt_jvm = self._jt_jvm
        if jobject.getClass() == jt_jvm.JClass(None, jt_jvm._jvm.String.Class, own=False):
            # Special case: String objects get converted to unicode,
            # which makes sense. They can get converted back if need be.
            with jt_jvm as (jvm, jenv):
                return JString(jenv, jobject.handle, own=False).str
        else:
            from .._javawrapper import wrap_instance
            return wrap_instance(jobject)

    def callInstance(self, meth, this, args):
        jobject = meth.callInstanceObject(this, args)
        if jobject is None:
            return None
        jt_jvm = self._jt_jvm
        if jobject.getClass() == jt_jvm.JClass(None, jt_jvm._jvm.String.Class, own=False):
            # Special case: String objects get converted to unicode,
            # which makes sense. They can get converted back if need be.
            with jt_jvm as (jvm, jenv):
                return JString(jenv, jobject.handle, own=False).str
        else:
            from .._javawrapper import wrap_instance
            return wrap_instance(jobject)
