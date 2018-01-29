# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from . import __config__ ; del __config__
from .__about__ import * ; del __about__

from ._main   import start, getclass
from ._pyjava import Error, ClassNotFound, NoMatchingOverload, FieldTypeError

__all__ = ('start', 'getclass',
           'Error', 'ClassNotFound', 'NoMatchingOverload', 'FieldTypeError')
