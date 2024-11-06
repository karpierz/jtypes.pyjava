# Copyright (c) 2016 Adam Karpierz
# SPDX-License-Identifier: MIT

from ._platform import JVMFinder
find_dll = lambda JVMFinder=JVMFinder: JVMFinder().find_dll()
del JVMFinder
