# Copyright (c) 2016 Adam Karpierz
# SPDX-License-Identifier: MIT

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
