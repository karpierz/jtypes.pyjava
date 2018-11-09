# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from . import _pyjava


def start(path=None, *args):

    from ._platform import JVMFinder

    if path is None:
        finder = JVMFinder()
        path = finder.get_jvm_path()

    if len(args) == 1 and isinstance(args[0], (list, tuple)):  # <AK> add tuple
        args = args[0]

    try:
        _pyjava.start(path, args)
    except Error:
        raise Error("Unable to start Java VM with path {}".format(path))


def getclass(class_name):

    # Convert from the 'usual' syntax to the 'JNI' syntax
    jni_class_name = class_name.replace(".", "/")

    return _pyjava.getclass(jni_class_name)  # might raise ClassNotFound
