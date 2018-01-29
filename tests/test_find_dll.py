# coding: utf-8

#<AK> added
#

from __future__ import absolute_import

import unittest

from .base import PyjavaTestCase

from jt.pyjava.find_dll import find_dll


class Test_find_dll(PyjavaTestCase):

    def test_find_dll(self):

        dll = find_dll()
        self.assertIsNotNone(dll)