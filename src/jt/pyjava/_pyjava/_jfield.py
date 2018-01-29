# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from ...jvm.lib import public

public(FIELD_STATIC    = 0x1)
public(FIELD_NONSTATIC = 0x2)
public(FIELD_BOTH      = (FIELD_STATIC | FIELD_NONSTATIC))
