# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from ...jvm.lib import public
from ...jvm.lib import enumc
from ...jvm import EJavaType
from ...jvm import EJavaModifiers

public(EJavaType      = EJavaType)
public(EJavaModifiers = EJavaModifiers)

public(
EMatchType = enumc(
    NONE     =   0,
    EXPLICIT =   1,
    IMPLICIT =  10,
    PERFECT  = 100,
))
