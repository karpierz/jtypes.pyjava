# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from __future__ import absolute_import

from ...jvm.lib.compat import *
from ...jvm.lib import annotate


@annotate('jt.jvm.JObject', utf8=bytes)
def from_utf8(utf8):

    # Create a Java string from standard UTF-8.
    #
    # Java's string functions expect a modified UTF-8 encoding which noone else uses.
    # These functions allow to use regular UTF-8, like Python does.
    #
    # @param utf8 Standard UTF-8 representation of the string; might contain null bytes.
    # @return A reference (as jvm.JObject) to a String object.
    #
    # Equivalent of: string = new String(utf8, "UTF-8");

    from ctypes import c_char_p
    from ...    import jni
    from ...jvm.jframe import JFrame
    from ._jvm  import JVM

    with JVM.jvm as (jvm, jenv), JFrame(jenv, 3):
        jbarr = jenv.NewByteArray(len(utf8))
        jutf8 = jenv.NewStringUTF(b"UTF-8")
        jenv.SetByteArrayRegion(jbarr, 0, len(utf8),
                                jni.cast(c_char_p(utf8), jni.POINTER(jni.jbyte)))
        String_Constructor_bytes = jenv.GetMethodID(jvm.String.Class,
                                                    b"<init>", b"([BLjava/lang/String;)V")
        jargs = jni.new_array(jni.jvalue, 2)
        jargs[0].l = jbarr
        jargs[1].l = jutf8
        jstr = jni.cast(jenv.NewObject(jvm.String.Class,
                                       String_Constructor_bytes, jargs), jni.jstring)
        return JVM.jvm.JObject(jenv, jstr)
