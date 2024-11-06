# Copyright (c) 2016 Adam Karpierz
# SPDX-License-Identifier: MIT

from . import __config__ ; del __config__
from .__about__ import * ; del __about__  # noqa

from ._main   import start, getclass
from ._pyjava import Error, ClassNotFound, NoMatchingOverload, FieldTypeError

__all__ = ('start', 'getclass',
           'Error', 'ClassNotFound', 'NoMatchingOverload', 'FieldTypeError')
