# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from __future__ import absolute_import

from ...jvm.lib.compat import *
from ...jvm.lib import annotate
from ...jvm     import jni


@annotate(jni.jstring, utf8=bytes)
def from_utf8(utf8):

    # Create a Java string from standard UTF-8.
    #
    # Java's string functions expect a modified UTF-8 encoding which noone else uses.
    # These functions allow to use regular UTF-8, like Python does.
    #
    # @param utf8 Standard UTF-8 representation of the string; might contain null bytes.
    # @return A reference to a String object, which you might want to clear.

    # string = new String(utf8, "UTF-8");

    from ctypes import c_char_p
    from ._jvm  import JVM

    jvm  = JVM.jvm
    jenv = JVM.jenv

    size  = len(utf8)
    jbarr = jenv.NewByteArray(size)
    jutf8 = jenv.NewStringUTF(b"UTF-8")
    try:
        jenv.SetByteArrayRegion(jbarr, 0, size, jni.cast(c_char_p(utf8), jni.POINTER(jni.jbyte)))
        String_Constructor_bytes = jenv.GetMethodID(jvm._jvm.String.Class,
                                                    b"<init>", b"([BLjava/lang/String;)V")
        jargs = jni.new_array(jni.jvalue, 2)
        jargs[0].l = jbarr
        jargs[1].l = jutf8
        return jni.cast(jenv.NewObject(jvm._jvm.String.Class,
                                       String_Constructor_bytes, jargs), jni.jstring)
    finally:
        jenv.DeleteLocalRef(jbarr)
        jenv.DeleteLocalRef(jutf8)
