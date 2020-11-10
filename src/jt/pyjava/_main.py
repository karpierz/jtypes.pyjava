# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from typing import Optional, List, Tuple

from . import _pyjava


def start(path: Optional[str] = None, *args):

    from ._platform import JVMFinder
    from ._pyjava   import Error

    if path is None:
        finder = JVMFinder()
        path = finder.get_jvm_path()

    if len(args) == 1 and isinstance(args[0], (List, Tuple)):  # <AK> add Tuple
        args = args[0]

    try:
        _pyjava.start(path, args)
    except Error:
        raise Error("Unable to start Java VM with path {}".format(path)) from None


def getclass(class_name: str):
    # Convert from the 'usual' syntax to the 'JNI' syntax
    jni_class_name = class_name.replace(".", "/")
    return _pyjava.getclass(jni_class_name)  # might raise ClassNotFound
