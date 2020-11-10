# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from ._platform import JVMFinder
find_dll = lambda JVMFinder=JVMFinder: JVMFinder().find_dll()
del JVMFinder
