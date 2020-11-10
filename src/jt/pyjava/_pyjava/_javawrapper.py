# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

"""
Non-public functions of javawrapper.

"""

from typing import Optional, Union, Tuple

from ._jclass  import JavaClass, JavaInstance
from ._jmethod import Constructor


def wrap_class(jclass: 'jvm.JClass') -> JavaClass:
    # Build a Python wrapper for a Java class.

    klass = JavaClass()
    klass._jclass     = jclass
    klass.constructor = Constructor()
    klass.constructor._jclass   = jclass
    klass.constructor.overloads = JavaClass._list_overloads(jclass)
    return klass


def wrap_instance(jobject: 'jvm.JObject') -> Union[JavaClass, JavaInstance]:
    # Wraps a JavaInstance object.

    jclass = jobject.getClass()

    if jclass == jclass.jvm.JClass(None, jclass.jvm._jvm.Class.Class, own=False):
        jclass = jobject.asClass()
        return wrap_class(jclass)
    else:
        jinstance = JavaInstance()
        jinstance._jobject = jobject
        return jinstance


def unwrap_instance(pyobject: object, with_javaclass: bool = False) \
    -> Tuple[Optional['jvm.JObject'], Optional['jvm.JClass']]:
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
        jclass  = (jclass.jvm.JClass(None, jclass.jvm._jvm.Class.Class, own=False)
                   if with_javaclass else None)
    else:
        jobject = None
        jclass  = None
    return (jobject, jclass)
