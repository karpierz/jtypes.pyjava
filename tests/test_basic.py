# <AK> added
#

import unittest

from .base import PyjavaTestCase

import _pyjava


class Test_basic(PyjavaTestCase):

    def test_from_utf8(self):
        from_utf8 = _pyjava._util.from_utf8
        expected = "Expected string"
        self.assertEqual(from_utf8(expected.encode("utf-8")).toString(), expected)
        expected = "Expected/0string"
        self.assertEqual(from_utf8(expected.encode("utf-8")).toString(), expected)
