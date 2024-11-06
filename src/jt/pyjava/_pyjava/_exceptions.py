# Copyright (c) 2016 Adam Karpierz
# SPDX-License-Identifier: MIT

from jvm.lib import public


@public
class Error(Exception):
    """ """

@public
class ClassNotFound(Error):
    """ """

@public
class NoMatchingOverload(Error, TypeError):
    __doc__ = TypeError.__doc__

@public
class FieldTypeError(Error, TypeError, AttributeError):
    __doc__ = TypeError.__doc__
