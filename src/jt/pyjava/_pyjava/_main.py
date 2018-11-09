# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from ...jvm.lib.compat import *
from ...jvm.lib import annotate, Union, Tuple, List

from ._jclass     import JavaClass
from ._exceptions import Error, ClassNotFound


@annotate(bool, path=Union[builtins.str, str], options=Union[Tuple, List])
def start(path, options):

    """
    start(str, list) -> bool

    Starts a Java Virtual Machine.
    The first argument is the path of the library to be dynamically loaded.
    The second is a list of strings that are passed to the JVM as options.

    """
    from ._jvm import JVM

    if JVM.jenv is not None:
        raise Error("Attempt to start() the JVM a second time.")

    if not all(isinstance(option, builtins.str) for option in options):
        raise TypeError("Options list contained non-string objects.")

    jvm = JVM(path.encode("utf-8").decode("utf-8"))
    jvm.start(*options, ignoreUnrecognized=True)

    return JVM.jenv is not None


@annotate(JavaClass, class_name=Union[builtins.str, str])
def getclass(class_name):

    """
    getclass(str) -> JavaClass

    Find the desired class and returns a wrapper.

    """
    from ._jvm import JVM
    from ._javawrapper import wrap_class

    if JVM.jenv is None:
        raise Error("Java VM is not running.")

    name_trans = JVM.jvm.JClass.name_trans
    class_name = class_name.encode("utf-8").translate(name_trans).decode("utf-8")

    try:
        javaclass = JVM.jvm.JClass.forName(class_name)
    except:
        raise ClassNotFound(class_name)

    return wrap_class(javaclass)
