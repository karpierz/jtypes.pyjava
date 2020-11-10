# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

import sys
import os
from os import path
import re

from jvm.lib import public
from jvm.lib import platform

from jvm.platform import _jvmfinder


@public
class JVMFinder(_jvmfinder.JVMFinder):

    def __init__(self, java_version=None):
        super().__init__(java_version)

        self._methods = (
            self.find_dll,
        )

    def find_dll(self):
        """Attempts to find the location of a JRE."""

        java_home = os.getenv("JAVA_HOME")

        # If JAVA_HOME is set, only consider this one
        if java_home:
            java_home_jre = path.join(java_home, "jre")
            # JAVA_HOME might be set to a JDK; in that case we use the 'jre' subdirectory
            if path.exists(java_home_jre):
                java_home = [java_home_jre]
                sys.stderr.write("Using JRE from JAVA_HOME environment variable (in jre/ subdir)\n")
            else:
                java_home = [java_home]
                sys.stderr.write("Using JRE from JAVA_HOME environment variable\n")
        # Else, consider all the dirs in /usr/lib/jvm
        else:
            java_home = []
            for directory in os.listdir("/usr/lib/jvm"):
                if directory[0] != ".":
                    directory = path.join("/usr/lib/jvm", directory)
                    java_home.append(directory)

            # Sort these possible homes
            def key(d):
                USUAL_NAME = re.compile(r"^.+/java-([0-9]+)-[^/]+$")
                m = USUAL_NAME.match(d)
                r = 0 if m is None else -int(m.group(1))
                # If on 32 bits, put "i386" installs at the start, else put them at the end
                if (platform.is_32bit and "i386" not in d) or (not platform.is_32bit and "i386" in d):
                    return r + 100
                else:
                    return r

            java_home = sorted(java_home, key=key)

        # Find the DLL
        for d in java_home:
            d = path.join(d, "lib")
            if path.isdir(d):
                for dd in os.listdir(d):
                    dd = path.join(d, dd)
                    if path.isdir(dd):
                        for ddd in ("client", "server"):
                            dll_file = path.join(dd, ddd, "libjvm.so")
                            if path.isfile(dll_file):
                                return dll_file
        return None
