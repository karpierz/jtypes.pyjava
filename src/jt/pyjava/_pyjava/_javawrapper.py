# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

"""
Non-public functions of javawrapper.

"""

from ...jvm.lib.compat import *
from ...jvm.lib import annotate, Optional, Union, Tuple

from ._jclass  import JavaClass, JavaInstance
from ._jmethod import Constructor


@annotate(JavaClass, jclass='jt.jvm.JClass')
def wrap_class(jclass):

    # Build a Python wrapper for a Java class.

    klass = JavaClass()
    klass._jclass     = jclass
    klass.constructor = Constructor()
    klass.constructor._jclass   = klass._jclass
    klass.constructor.overloads = JavaClass._list_overloads(klass.constructor._jclass)
    return klass


@annotate(Union[JavaClass, JavaInstance], jobject='jt.jvm.JObject')
def wrap_instance(jobject):

    # Wraps a JavaInstance object.

    jclass = jobject.getClass()

    if jclass == jclass.jvm.JClass(None, jclass.jvm._jvm.Class.Class, borrowed=True):
        jclass = jobject.asClass()
        return wrap_class(jclass)
    else:
        jinstance = JavaInstance()
        jinstance._jobject = jobject
        return jinstance


@annotate(Tuple[Optional['jt.jvm.JObject'], Optional['jt.jvm.JClass']],
          pyobject=object, with_javaclass=bool)
def unwrap_instance(pyobject, with_javaclass=False):

    # Unwraps a JavaInstance object.
    #
    # @param with_javaclass Where to store the Java class.
    # @returns (jobject, jclass) on success, (None, None) on error
    #          (for instance, pyobj wasn't a JavaInstance Python object).

    if isinstance(pyobject, JavaInstance):
        jobject = pyobject._jobject
        jobject = jobject.jvm.JObject.fromObject(jobject)
        jclass  = jobject.getClass() if with_javaclass else None
    elif isinstance(pyobject, JavaClass):
        jclass  = pyobject._jclass
        jobject = jclass.asObject()
        jclass  = (jclass.jvm.JClass(None, jclass.jvm._jvm.Class.Class, borrowed=True)
                   if with_javaclass else None)
    else:
        jobject = None
        jclass  = None
    return (jobject, jclass)
