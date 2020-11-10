# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public

from ._constants  import EMatch
from ._constants  import EJavaModifiers
from ._jfield     import FIELD_STATIC, FIELD_NONSTATIC, FIELD_BOTH
from ._jmethod    import UnboundMethod, BoundMethod, ClassMethod, JavaMethodOverload
from ._exceptions import FieldTypeError


@public
class JavaClass:
    """Java class wrapper"""

    # "pyjava.JavaClass" # tp_name
    # Equivalent of: jt.jtypes.JavaClass

    # JavaClass type.
    #
    # This is the wrapper returned by getclass().
    # It can be called to make a new instance of that Java type,
    # or accessed for either static fields or unbound methods (static or not).

    def __new__(cls, *args, **kwargs):
        if len(args) != 0:
            raise NotImplementedError("Subclassing Java classes is not supported")
        self = super().__new__(cls)
        self._jclass     = None
        self.constructor = None
        return self

    __hash__ = None

    def __subclasscheck__(self, subclass):
        if not isinstance(subclass, JavaClass):
            return False
        return self._jclass.isAssignableFrom(subclass._jclass)

    def __instancecheck__(self, instance):
        if not isinstance(instance, JavaInstance):
            return False
        return self._jclass.isAssignableFrom(instance._jobject.getClass())

    def __call__(self, *args, **kwargs):
        return self.constructor(*args)

    def __getattr__(self, name):

        jclass = self._jclass.jvm.JClass(None, self._jclass.jvm._jvm.Class.Class, own=False)
        is_class_class = self._jclass.asObject(own=False) == jclass.asObject(own=False)

        # First, try to find a method with that name, in that class.
        # If at least one such method exists, we return an UnboundMethod.
        if not is_class_class:
            overloads = JavaClass._list_overloads(self._jclass, name, FIELD_BOTH)
            if overloads:
                unbound_method = UnboundMethod()
                unbound_method.name      = name
                unbound_method._jclass   = self._jclass
                unbound_method.overloads = overloads
                return unbound_method

        # Then, try a field (static)
        try:
            try:
                jfield = self._jclass.getField(name.encode("utf-8").decode("utf-8"))
            except Exception:
                raise AttributeError("no field with that name") from None

            mods = jfield.getModifiersSet()
            is_static = EJavaModifiers.STATIC in mods
            if not is_static:
                raise AttributeError("field doesn't have the required type")

            thandler = jfield.jvm.type_manager.get_handler(jfield.getType())
            return thandler.getStatic(jfield, self._jclass)

        except AttributeError:
            pass

        # Finally, act on the Class object (reflection)
        # If calling from Class, we can access all methods;
        # if calling on another Class instance, don't access the static methods
        what = FIELD_BOTH if is_class_class else FIELD_NONSTATIC
        overloads = JavaClass._list_overloads(jclass, name, what)
        if overloads:
            # A different kind of wrapper is used here because we need a
            # non-static Class method to be bound to javaclass but a static
            # Class method not to be (obviously, it's static).
            class_method = ClassMethod()
            class_method.name      = name
            class_method._jclass   = self._jclass
            class_method.overloads = overloads
            return class_method

        # We didn't find anything
        raise AttributeError("Java class has no attribute {}".format(name))

    def __setattr__(self, name, value):

        if name in ("_jclass", "constructor"):
            super().__setattr__(name, value)
            return

        from ..__config__ import config

        try:
            try:
                jfield = self._jclass.getField(name.encode("utf-8").decode("utf-8"))
            except Exception:
                raise AttributeError("no field with that name") from None

            mods = jfield.getModifiersSet()
            is_static = EJavaModifiers.STATIC in mods
            if not is_static:
                raise AttributeError("field doesn't have the required type")

            thandler = jfield.jvm.type_manager.get_handler(jfield.getType())

            if thandler.match(value) <= EMatch.EXPLICIT:
                raise FieldTypeError("Java static attribute {} has incompatible type".format(
                                     name))

            if config.getboolean("WITH_VALID", False) and not thandler.valid(value):
                raise ValueError("Assigned value is not valid for required field type.")

            thandler.setStatic(jfield, self._jclass, value)

        except FieldTypeError:
            raise
        except AttributeError:
            raise AttributeError("Java class has no static attribute {}".format(name)) from None

    def __eq__(self, other):

        # raise TypeError("JavaClass only supports == and !=")

        if self is other:
            return True

        if not isinstance(other, (JavaClass, JavaInstance)):
            return False

        self_jobject  = self._jclass.asObject(own=False)
        other_jobject = (other._jclass.asObject(own=False)
                         if isinstance(other, JavaClass) else other._jobject)

        return self_jobject == other_jobject

    def __ne__(self, other):
        eq = self.__eq__(other)
        return NotImplemented if eq is NotImplemented else not eq

    @classmethod
    def _list_overloads(cls, jclass, method_name=None, what=None):

        constructors = method_name is None
        if constructors:
            method_name, what = b"<init>", FIELD_STATIC
            is_static = True

        # Create the list of methods.
        # FIXME : we could count the exact number of methods we'll need to store,
        #         instead of using the total array length as an upper bound.
        overloads = []
        for jmeth in (jclass.getConstructors() if constructors else jclass.getMethods()):

            if not constructors:
                if jmeth.getName().encode("utf-8") != method_name.encode("utf-8"):
                    continue
                mods = jmeth.getModifiersSet()
                is_static = EJavaModifiers.STATIC in mods

            if ((is_static     and not (what & FIELD_STATIC)) or
                (not is_static and not (what & FIELD_NONSTATIC))):
                continue

            ovr = JavaMethodOverload(jmeth)
            ovr._is_static = is_static

            overloads.append(ovr)

        return tuple(overloads) if overloads else None


@public
class JavaInstance:
    """Java object wrapper"""

    # "pyjava.JavaInstance" # tp_name
    # Equivalent of: jt.jtypes.JavaObject

    # JavaInstance type.
    #
    # This is the wrapper for Java instance objects; it contains a jobject.

    def __new__(cls):
        self = super().__new__(cls)
        self._jobject = None
        return self

    __hash__ = None

    def __getattr__(self, name):

        jclass = self._jobject.getClass()

        # First, try to find a method with that name, in that class.
        # If at least one such method exists, we return a BoundMethod.
        overloads = JavaClass._list_overloads(jclass, name, FIELD_BOTH)
        if overloads:
            bound_method = BoundMethod()
            bound_method.name       = name
            bound_method._jclass    = jclass
            bound_method._jinstance = self._jobject
            bound_method.overloads  = overloads
            return bound_method

        # Then, try a field (nonstatic)
        try:
            try:
                jfield = jclass.getField(name.encode("utf-8").decode("utf-8"))
            except Exception:
                raise AttributeError("no field with that name") from None

            mods = jfield.getModifiersSet()
            is_static = EJavaModifiers.STATIC in mods
            if is_static:
                raise AttributeError("field doesn't have the required type")

            thandler = jfield.jvm.type_manager.get_handler(jfield.getType())
            return thandler.getInstance(jfield, self._jobject)

        except AttributeError:
            raise AttributeError("Java instance has no attribute {}".format(name)) from None

    def __setattr__(self, name, value):

        if name in ("_jobject",):
            super().__setattr__(name, value)
            return

        from ..__config__ import config

        jclass = self._jobject.getClass()

        try:
            try:
                jfield = jclass.getField(name.encode("utf-8").decode("utf-8"))
            except Exception:
                raise AttributeError("no field with that name") from None

            mods = jfield.getModifiersSet()
            is_static = EJavaModifiers.STATIC in mods
            if is_static:
                raise AttributeError("field doesn't have the required type")

            thandler = jfield.jvm.type_manager.get_handler(jfield.getType())

            if thandler.match(value) <= EMatch.EXPLICIT:
                raise FieldTypeError("Java nonstatic attribute {} has incompatible type".format(
                                     name))

            if config.getboolean("WITH_VALID", False) and not thandler.valid(value):
                raise ValueError("Assigned value is not valid for required field type.")

            thandler.setInstance(jfield, self._jobject, value)

        except FieldTypeError:
            raise
        except AttributeError:
            raise AttributeError("Java class has no nonstatic attribute {}".format(
                                 name)) from None

    def __eq__(self, other):

        # raise TypeError("JavaInstance only supports == and !=")

        if self is other:
            return True

        if not isinstance(other, (JavaInstance, JavaClass)):
            return False

        self_jobject  = self._jobject
        other_jobject = (other._jclass.asObject(own=False)
                         if isinstance(other, JavaClass) else other._jobject)

        return self_jobject == other_jobject

    def __ne__(self, other):
        eq = self.__eq__(other)
        return NotImplemented if eq is NotImplemented else not eq
