# Copyright (c) 2015-2020 Adam Karpierz
# Licensed under the MIT License
# https://opensource.org/licenses/MIT

import unittest
import sys
import os
import importlib
import logging

from . import test_dir

log = logging.getLogger(__name__)


def test_suite(names=None, omit=("run", "base")):
    from . import __name__ as pkg_name
    from . import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if name != "__main__" and not name.startswith("tman_")
                 and name not in omit]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def main(argv=sys.argv):

    sys.modules["pyjava"]          = importlib.import_module("jt.pyjava")
    sys.modules["pyjava.find_dll"] = importlib.import_module("jt.pyjava.find_dll")
    sys.modules["_pyjava"]         = importlib.import_module("jt.pyjava._pyjava")

    print("Running testsuite", "\n", file=sys.stderr)

    try:
        tests = test_suite(argv[1:] or None)
        result = unittest.TextTestRunner(verbosity=2).run(tests)
    finally:
        pass

    return 0 if result.wasSuccessful() else 1


if __name__.rpartition(".")[-1] == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
