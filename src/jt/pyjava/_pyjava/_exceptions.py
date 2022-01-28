# Copyright (c) 2016-2022 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

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
