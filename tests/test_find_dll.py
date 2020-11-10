# <AK> added
#

import unittest

from .base import PyjavaTestCase

from pyjava.find_dll import find_dll


class Test_find_dll(PyjavaTestCase):

    def test_find_dll(self):
        dll = find_dll()
        self.assertIsNotNone(dll)
