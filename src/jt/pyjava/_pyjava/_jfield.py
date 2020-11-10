# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

from jvm.lib import public

public(FIELD_STATIC      = 0x01)
public(FIELD_NONSTATIC   = 0x02)
public(FIELD_BOTH        = (FIELD_STATIC | FIELD_NONSTATIC))
public(FIELD_CONSTRUCTOR = 0x80)
