# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from typing import Optional

from jvm.lib import public
from jvm.lib import classproperty
import jni

from jvm import JVM as _JVM


@public
class JVM(_JVM):
    """Represents the Java virtual machine"""

    jvm  = classproperty(lambda cls: JVM._jvm)
    jenv = classproperty(lambda cls: JVM._jenv)

    _jvm  = None  # Optional[jvm.JVM]
    _jenv = None  # Optional[jvm.jni.JNIEnv]

    def __init__(self, dll_path=None):
        from ._typemanager import TypeManager
        self._dll_path = None
        self._load(dll_path)
        self.type_manager = TypeManager()

    def start(self, *jvmoptions, **jvmargs):
        _, jenv = result = super().start(*jvmoptions, **jvmargs)
        JVM._jvm, JVM._jenv = self, jenv
        self.type_manager.start()
        return result

    def shutdown(self):
        self.type_manager.stop()
        _, jenv = self
        super().shutdown()
        JVM._jvm = JVM._jenv = None

    def _load(self, dll_path=None):
        from jvm.platform import JVMFinder
        from jvm          import EStatusCode
        if dll_path is not None:
            self._dll_path = dll_path
        elif self._dll_path is None:
            finder = JVMFinder()
            self._dll_path = finder.get_jvm_path()
        super().__init__(self._dll_path)
