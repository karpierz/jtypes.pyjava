# Copyright (c) 2015-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

from __future__ import absolute_import, print_function

import unittest
import sys
import os
import importlib
import logging

from . import test_dir


def test_suite(names=None, omit=("run", "base")):

    from . import __name__ as pkg_name
    from . import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if name != "__main__" and name not in omit]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def main():

    sys.modules["pyjava"]          = importlib.import_module("jt.pyjava")
    sys.modules["pyjava.find_dll"] = importlib.import_module("jt.pyjava.find_dll")
    sys.modules["_pyjava"]         = importlib.import_module("jt.pyjava._pyjava")

    print("Running testsuite", "\n", file=sys.stderr)

    try:
        tests = test_suite(sys.argv[1:] or None)
        result = unittest.TextTestRunner(verbosity=2).run(tests)
    finally:
        pass

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__.rpartition(".")[-1] == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    main()
