# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

import jni

from jvm.jframe import JFrame

from ._jvm import JVM


def from_utf8(utf8: bytes) -> 'jvm.JObject':
    # Create a Java string from standard UTF-8.
    #
    # Java's string functions expect a modified UTF-8 encoding.
    # These functions allow to use regular UTF-8, like Python does.
    #
    # @param utf8 Standard UTF-8 representation of the string;
    #             might contain null bytes.
    # @return A reference (as jvm.JObject) to a String object.
    #
    # Equivalent of: string = new String(utf8, "UTF-8");
    with JVM.jvm as (jvm, jenv), JFrame(jenv, 3):
        size = len(utf8)
        addr = jni.as_cstr(utf8)
        jarr = jenv.NewByteArray(size)
        jenv.SetByteArrayRegion(jarr, 0, size,
                                jni.cast(addr, jni.POINTER(jni.jbyte)))
        jutf8 = jenv.NewStringUTF(b"UTF-8")
        jargs = jni.new_array(jni.jvalue, 2)
        jargs[0].l = jarr
        jargs[1].l = jutf8
        jstr = jni.cast(jenv.NewObject(jvm.String.Class,
                                       jvm.String.ConstructorFromBytes,
                                       jargs), jni.jstring)
        return JVM.jvm.JObject(jenv, jstr)
