# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from __future__ import absolute_import

import sys
import os
import os.path as osp
import re
if sys.version_info.major >= 3:
    import winreg
else:
    import _winreg as winreg

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
            # JAVA_HOME might be set to a JDK; in that case we use the 'jre' subdirectory
            java_home_jre = osp.join(java_home, "jre")
            if osp.exists(java_home_jre):
                java_home = java_home_jre
                sys.stderr.write("Using JRE from JAVA_HOME environment variable (in jre/ subdir)\n")
            else:
                sys.stderr.write("Using JRE from JAVA_HOME environment variable\n")

            return osp.join(java_home, "bin", "client", "jvm.dll")
        else:
            program_files     = os.getenv("ProgramFiles", r"C:\Program Files")
            program_files_x86 = os.getenv("ProgramFiles(x86)")

            if program_files_x86 is not None and osp.exists(program_files_x86):
                # On Win64 in 32-bit mode: %ProgramFiles% ==> 'C:\Program Files (x86)'
                # On Win64 in 64-bit mode: %ProgramFiles% ==> 'C:\Program Files'
                java_home = self._find_jre(program_files + r"\Java")
            else:
                java_home = self._find_jre(program_files + r"\Java")

            return osp.join(java_home, "bin", "client", "jvm.dll")

    def _find_jre(self, java_dir):

        JRE_NAME1 = re.compile(r"^jre([0-9])$")
        JRE_NAME2 = re.compile(r"^jre([0-9])\.([0-9]+)\.([0-9]+)_([0-9]+)$")
        JDK_NAME  = re.compile(r"^jdk([0-9])\.([0-9]+)\.([0-9]+)_([0-9]+)$")

        if not osp.exists(java_dir):
            return None

        # Trying JREs
        choice = None
        for subdir in os.listdir(java_dir):
            for i, JRE_NAME in enumerate((JRE_NAME1, JRE_NAME2)):
                m = JRE_NAME.match(subdir)
                if m:
                    version = m.groups()
                    if i == 0:
                        version = ('1',) + version + ('0', '00')
                    if choice is None or version > choice[1]:
                        choice = subdir, version
        if choice is not None:
            return osp.join(java_dir, choice[0])

        # Trying JDKs
        choice = None
        for subdir in os.listdir(java_dir):
            m = JDK_NAME.match(subdir)
            if m:
                version = m.groups()
                if choice is None or version > choice[1]:
                    choice = subdir, version
        if choice is not None:
            return osp.join(java_dir, choice[0], "jre")

        return None
