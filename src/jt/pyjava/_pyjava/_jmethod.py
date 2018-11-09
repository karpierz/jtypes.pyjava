# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from __future__ import absolute_import

import collections as abcoll
import warnings

from ...jvm.lib.compat import *
from ...jvm.lib import annotate, Optional, Union, Tuple
from ...jvm.lib import public
from ...jvm.lib import cached

from ._constants  import EMatchType
from ._jfield     import FIELD_STATIC, FIELD_NONSTATIC, FIELD_BOTH
from ._exceptions import NoMatchingOverload


class JavaCallable(abcoll.Callable):

    # Equivalent of: jt.jtypes.JavaCallable

    def _match_overload(self, what, overloads, *args):

        best_ovrs  = []
        nonmatches = 0

        for ovr in overloads:

            # Attempt to match the arguments with the ones we got from Python.

            if ((ovr._is_static     and not (what & FIELD_STATIC)) or
                (not ovr._is_static and not (what & FIELD_NONSTATIC))):
                continue

            match_level = ovr.match_args(args)
            if match_level == EMatchType.NONE:
                nonmatches += 1
            else:
                best_ovrs.append(ovr)

        if len(best_ovrs) == 0:
            return None, nonmatches

        return best_ovrs[0] if len(best_ovrs) == 1 else best_ovrs, nonmatches


@public
class Constructor(JavaCallable):

    # Equivalent of: jt.jtypes.JavaConstructor

    def __new__(cls):

        self = super(Constructor, cls).__new__(cls)
        self._jclass   = None
        self.overloads = ()
        return self

    def __call__(self, *args, **kwargs):

        from ._jclass import JavaInstance

        if not self.overloads:
            raise NoMatchingOverload("no visible constructor")

        best_ovr, nonmatches = self._match_overload(FIELD_STATIC, self.overloads, *args)

        if best_ovr is None:
            raise NoMatchingOverload("{} constructors with {} parameters (no match)".format(
                                     nonmatches, len(args)))

        if isinstance(best_ovr, list):
            # Several constructors matched the given arguments.
            # We'll use the first constructor we found.
            # The Java compiler shouldn't let this happen... may be a bug
            # in the convert module?
            best_ovr = best_ovr[0]
            warnings.warn("Multiple Java constructors matching Python parameters", RuntimeWarning)
            raise Exception("RuntimeWarning:" + " " +
                            "Multiple Java constructors matching Python parameters")

        instance = JavaInstance()
        instance._jobject = best_ovr.call_constructor(*args)
        return instance


class _Method(JavaCallable):

    def __new__(cls):

        self = super(_Method, cls).__new__(cls)
        self.name      = None
        self.overloads = ()
        return self

    @annotate(object, cls='jt.jvm.JClass', args=Tuple, what=int)
    def _call(self, cls, args, what):

        best_ovr, nonmatches = self._match_overload(what, self.overloads, *args)

        if best_ovr is None:
            raise NoMatchingOverload("{} methods with {} parameters (no match)".format(
                                     nonmatches, len(args)))

        if isinstance(best_ovr, list):
            # Several methods matched the given arguments.
            # We'll use the first method we found.
            # The Java compiler shouldn't let this happen... may be a bug
            # in the convert module?
            best_ovr = best_ovr[0]
            warnings.warn("Multiple Java methods matching Python parameters", RuntimeWarning)
            raise Exception("RuntimeWarning:" + " " +
                            "Multiple Java methods matching Python parameters")

        try:
            if best_ovr._is_static:
                return best_ovr.call_static(cls, *args)
            else:
                pdescr   = best_ovr._params_info[0]
                thandler = pdescr.thandler
                this = thandler.toJava(args[0])
                return best_ovr.call_instance(this, *args)
        except:  # ??? # if ret == NULL
            raise NoMatchingOverload("{} methods with {} parameters (no match)".format(
                                     nonmatches, len(args)))


@public
class UnboundMethod(_Method):

    """Java unbound method"""

    # "pyjava.UnboundMethod" # tp_name
    # Equivalent of: jt.jtypes.JavaMethod

    # This represents an unbound method, i.e. a method obtained from the class.
    # It has no instance associated with it. When called, it will be matched
    # with both the static and nonstatic methods of that class. It contains
    # the jclass and the name of the method.

    def __new__(cls):

        self = super(UnboundMethod, cls).__new__(cls)
        self._jclass = None
        return self

    javaclass = property(lambda self: self._jclass.handle)

    def __call__(self, *args, **kwargs):

        best_ovr, nonmatches = self._match_overload(FIELD_BOTH, self.overloads, *args)

        if best_ovr is None:
            raise NoMatchingOverload("{} methods with {} parameters (no match)".format(
                                     nonmatches, len(args)))

        if isinstance(best_ovr, list):
            # Several methods matched the given arguments.
            # We'll use the first method we found.
            # The Java compiler shouldn't let this happen... may be a bug
            # in the convert module?
            best_ovr = best_ovr[0]
            warnings.warn("Multiple Java methods matching Python parameters", RuntimeWarning)
            raise Exception("RuntimeWarning:" + " " +
                            "Multiple Java methods matching Python parameters")

        try:
            if best_ovr._is_static:
                return best_ovr.call_static(self._jclass, *args)
            else:
                pdescr   = best_ovr._params_info[0]
                thandler = pdescr.thandler
                this = thandler.toJava(args[0])
                return best_ovr.call_instance(this, *args)
        except:  # ??? # if ret == NULL
            raise NoMatchingOverload("{} methods with {} parameters (no match)".format(
                                     nonmatches, len(args)))


@public
class BoundMethod(_Method):

    """Java bound method"""

    # "pyjava.BoundMethod" # tp_name
    # Equivalent of: jt.jtypes.JavaBoundMethod

    # This represents a bound method, i.e. a method obtained from an instance.
    # It is associated with the instance it was retrieved from. When called, it
    # will be matched only with the nonstatic methods of that class, and will use
    # the instance it is bound to as the self argument. It contains the jclass,
    # the jobject, and the name of the method.

    def __new__(cls):

        self = super(BoundMethod, cls).__new__(cls)
        self._jclass    = None
        self._jinstance = None
        return self

    javaclass    = property(lambda self: self._jclass.handle)
    javainstance = property(lambda self: self._jinstance.handle)

    def __call__(self, *args, **kwargs):

        from ._javawrapper import wrap_instance

        wjinstance = wrap_instance(self._jinstance)
        bound_args = (wjinstance,) + args

        best_ovr, nonmatches = self._match_overload(FIELD_NONSTATIC, self.overloads, *bound_args)

        if best_ovr is None:
            raise NoMatchingOverload("{} methods with {} parameters (no match)".format(
                                     nonmatches, len(bound_args)))

        if isinstance(best_ovr, list):
            # Several methods matched the given arguments.
            # We'll use the first method we found.
            # The Java compiler shouldn't let this happen... may be a bug
            # in the convert module?
            best_ovr = best_ovr[0]
            warnings.warn("Multiple Java methods matching Python parameters", RuntimeWarning)
            raise Exception("RuntimeWarning:" + " " +
                            "Multiple Java methods matching Python parameters")

        try:
            pdescr   = best_ovr._params_info[0]
            thandler = pdescr.thandler
            this = thandler.toJava(wjinstance)
            # return best_ovr.call_instance(this, *bound_args)
            return best_ovr.call_instance(this, *args)
        except:  # ??? # if ret == NULL
            raise NoMatchingOverload("{} methods with {} parameters (no match)".format(
                                     nonmatches, len(bound_args)))


@public
class ClassMethod(_Method):

    """Java class method"""

    # "pyjava.ClassMethod" # tp_name

    # This represents a Class method obtained from a JavaClass.
    # If the class is Java's Class, 'overloads' contains methods that are static
    # or unbound. If a non-static method is called, we don't want it to be bound
    # to Class but rather to use the first argument as 'self'.
    # It contains the jclass, the jobject, and the name of the method.

    def __new__(cls):

        self = super(ClassMethod, cls).__new__(cls)
        self._jclass = None
        return self

    javaclass = property(lambda self: self._jclass.handle)

    def __call__(self, *args, **kwargs):

        from ._javawrapper import wrap_class

        jclass = self._jclass.jvm.JClass(None, self._jclass.jvm._jvm.Class.Class, borrowed=True)

        # Attempts bound method call

        bound_args = (wrap_class(self._jclass),) + args
        try:
            return self._call(jclass, bound_args, FIELD_NONSTATIC)
        except:  # ???
            del bound_args
            # Attempts unbound method call
            return self._call(self._jclass, args, FIELD_BOTH)


@public
class JavaMethodOverload(object):

    # Equivalent of: jt.jtypes.JavaMethodOverload

    class ParamInfo(object):

        __slots__ = ('thandler', 'is_mutable', 'is_output')

        def __init__(self, thandler):

            self.thandler   = thandler
            self.is_mutable = False
            self.is_output  = False

    class ReturnInfo(object):

        __slots__ = ('thandler',)

        def __init__(self, thandler):

            self.thandler = thandler

    def __new__(cls, overload):

        self = super(JavaMethodOverload, cls).__new__(cls)
        self.__jmethod    = overload  # Union[jt.jvm.JConstructor, jt.jvm.JMethod]
        self._params_info = None
        self._return_info = None
        self._is_static   = False
        return self

    @cached
    def __init(self):

        type_manager = self.__jmethod.jvm.type_manager
        # Store the parameters
        param_types = []
        if not self._is_static:  # also if not constructors
            # Is the method static ?
            # If not, we'll add a first parameter of this class's type.
            # In Python, non-static methods take a first "self" parameter
            # that can be made implicit through the "binding" mechanism
            param_types.append(self.__jmethod.getDeclaringClass())
        for jclass in self.__jmethod.getParameterTypes():
            param_types.append(jclass)
        self._params_info = tuple(self.ParamInfo(type_manager.get_handler(jclass))
                                  for jclass in param_types)
        # Store the return type
        if isinstance(self.__jmethod, self.__jmethod.jvm.JMethod):
            jclass = self.__jmethod.getReturnType()
            self._return_info = self.ReturnInfo(type_manager.get_handler(jclass))
        else:
            self._return_info = None

    def match_args(self, args):

        self.__init()

        arg_count  = len(args)
        par_descrs = self._params_info
        par_count  = len(par_descrs)

        if arg_count != par_count:
            return EMatchType.NONE

        best_match = EMatchType.PERFECT
        for pdescr, arg in zip(par_descrs, args):
            match_level = pdescr.thandler.match(arg)
            if match_level == EMatchType.NONE:
                return EMatchType.NONE
            if match_level < best_match:
                best_match = match_level

        return best_match

    def call_constructor(self, *args):

        jargs  = self.__make_arguments(args)
        result = self.__jmethod.newInstance(jargs)
        self.__close_arguments(jargs, args)
        return result

    def call_static(self, jclass, *args):

        jargs  = self.__make_arguments(args)
        result = self._return_info.thandler.callStatic(self.__jmethod, jclass, jargs)
        self.__close_arguments(jargs, args)
        return result

    def call_instance(self, this, *args):

        jargs  = self.__make_arguments(args)
        result = self._return_info.thandler.callInstance(self.__jmethod, this, jargs)
        self.__close_arguments(jargs, args)
        return result

    def __make_arguments(self, args):

        from ..__config__ import config

        self.__init()

        arg_count  = len(args)
        par_descrs = self._params_info
        pos0       = 0 if self._is_static else 1

        jargs = self.__jmethod.jvm.JArguments(arg_count)
        for pos in range(pos0, arg_count):
            pdescr   = par_descrs[pos]
            arg      = args[pos]
            thandler = pdescr.thandler
            if config.getboolean("WITH_VALID", False) and not thandler.valid(arg):
                raise ValueError("Parameter value is not valid for required parameter type.")
            thandler.setArgument(pdescr, jargs, pos - pos0, arg)

        return jargs

    def __close_arguments(self, jargs, args):

        pass
