# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from __future__ import absolute_import

import os
from os import path

from ...jvm.platform import _jvmfinder


class JVMFinder(_jvmfinder.JVMFinder):

    def __init__(self, java_version=None):

        super(JVMFinder, self).__init__(java_version)

        self._methods = (
            self.find_dll,
        )

    def find_dll(self):

        """Attempts to find the location of a JRE."""

        java_home = os.getenv("JAVA_HOME")

        if java_home:
            if path.isdir(java_home):
                dll_file = path.join(java_home, "JavaVM")
                if path.isfile(dll_file):
                    return dll_file
        # Apparently the DLL is always at the same place on OSX
        return "/System/Library/Frameworks/JavaVM.framework/JavaVM"
