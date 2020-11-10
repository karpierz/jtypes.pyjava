# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from typing import Union, Tuple, List

from ._jclass     import JavaClass
from ._exceptions import Error, ClassNotFound


def start(path: str, options: Union[Tuple, List]) -> bool:
    """
    start(str, list) -> bool

    Starts a Java Virtual Machine.
    The first argument is the path of the library to be dynamically loaded.
    The second is a list of strings that are passed to the JVM as options.

    """
    from ._jvm import JVM

    if JVM.jenv is not None:
        raise Error("Attempt to start() the JVM a second time.")

    if not all(isinstance(option, str) for option in options):
        raise TypeError("Options list contained non-string objects.")

    jvm = JVM(path.encode("utf-8").decode("utf-8"))
    jvm.start(*options, ignoreUnrecognized=True)

    return JVM.jenv is not None


def getclass(class_name: str) -> JavaClass:
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
    except Exception:
        raise ClassNotFound(class_name) from None

    return wrap_class(javaclass)
