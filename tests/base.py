import sys
import unittest  # <AK> removed unittest2 requirement

from . import test_dir  # <AK> added


class PyjavaTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hasattr(PyjavaTestCase, '_pyjava_started'):
            return

        import _pyjava
        from pyjava.find_dll import find_dll


        dll = find_dll()
        if not dll:
            sys.stderr.write("No suitable JVM DLL found. Please set your JAVA_HOME "
                             "environment variable.\n")
            sys.exit(1)
        else:
            sys.stderr.write("Running tests with JVM DLL: %s\n" % dll)


        # This need to be called once, before running the test suite
        class_path = test_dir/"java-tests/classes"  # <AK> added
        _pyjava.start(dll, [f"-Djava.class.path={class_path}"])

        PyjavaTestCase._pyjava_started = True
