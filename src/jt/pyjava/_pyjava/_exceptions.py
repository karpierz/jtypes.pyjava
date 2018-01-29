# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from ...jvm.lib import public


@public
class Error(Exception):

    """ """

@public
class ClassNotFound(Error):

    """ """

@public
class NoMatchingOverload(Error, TypeError):

    """ """

@public
class FieldTypeError(Error, TypeError, AttributeError):

    """ """
