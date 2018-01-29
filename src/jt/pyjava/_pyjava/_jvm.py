# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from ...jvm.lib.compat import *
from ...jvm.lib import annotate, Optional
from ...jvm.lib import public

from ...jvm import JVM as _JVM


@public
class JVM(_JVM):

    """Represents the Java virtual machine"""

    jvm  = None  # Optional[jt.jvm.JVM]
    jenv = None  # Optional[jt.jvm.jni.JNIEnv]

    def __init__(self, dll_path=None):

        from ._typehandler import TypeHandler

        self._dll_path = None
        self.load(dll_path)
        self.type_handler = TypeHandler()

    def load(self, dll_path=None):

        from ...jvm.platform import JVMFinder
        from ...jvm          import EStatusCode

        if dll_path is not None:
            self._dll_path = dll_path

        if self._dll_path is None:
            finder = JVMFinder()
            self._dll_path = finder.get_jvm_path()

        super(JVM, self).__init__(self._dll_path)

    def start(self, *jvmoptions, **jvmargs):

        result = super(JVM, self).start(*jvmoptions, **jvmargs)
        self.type_handler.start()
        return result

    def shutdown(self):

        self.type_handler.stop()
        super(JVM, self).shutdown()


# eof
