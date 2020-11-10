# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

import enum

from jvm.lib import public

from jvm import EJavaType
from jvm import EJavaModifiers

public(EJavaType      = EJavaType)
public(EJavaModifiers = EJavaModifiers)

@public
class EMatch(enum.IntEnum):
    NONE     =   0
    EXPLICIT =   1
    IMPLICIT =  10
    PERFECT  = 100
