**Currently only as placeholder (because a base package jtypes.jvm is still in development)**

jtypes.pyjava
=============

A Python to Java bridge.

Overview
========

  | jtypes.pyjava is a bridge allowing to use Java classes in regular Python code.
  |
  | jtypes.pyjava is a lightweight Python package, based on the *ctypes* or *cffi* library.
  | It is an almost fully compliant implementation of Remi Rampin's *PyJava* package
    by reimplementing whole its functionality in a clean Python instead of C/C++.


About PyJava:
-------------

Borrowed from the `original website <https://github.com/remram44/pyjava/blob/master/README.md>`__:

    PyJava is a bridge allowing to use Java classes in regular Python code.
    It is similar to `JPype <http://jpype.sourceforge.net/>`__.

    It is a C extension that uses JNI to access a Java virtual machine,
    meaning that it can be used anywhere Python is available. It is not
    a different interpreter like `Jython <http://jython.org/>`__ and does
    not require anything, other than a JRE. The JVM dynamic library is load
    dynamically through pyjava.start() (some basic logic for locating this
    library on major platforms will be provided).

    The integration with Java code is meant to be as complete as possible,
    allowing to use Java and Python objects seemlessly and converting objects
    back and forth when Java code is called. Furthermore, subclassing Java
    classes or interfaces in Python code to allow callback from Java is planned
    for the 0.2 version.

    Please note that this extension is still at a very early stage of
    development and probably shouldn't be used for anything.

Requirements
============

- Either the Sun/Oracle JRE/JDK or OpenJDK.

Installation
============

To install run::

    python -m pip install --upgrade jtypes.pyjava

To ensure everything is running correctly you can run the tests using::

    python -m jt.pyjava.tests

Development
===========

Visit `development page <https://github.com/karpierz/jtypes.pyjava>`__

Installation from sources:

Clone the `sources <https://github.com/karpierz/jtypes.pyjava>`__ and run::

    python -m pip install ./jtypes.pyjava

or on development mode::

    python -m pip install --editable ./jtypes.pyjava

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install tox

Prerequisites:

+ Python 2.7 or higher or 3.4 or higher

  * http://www.python.org/
  * Versions lower than 2.7 or lower than 3.4 WON'T WORK.
  * 2.7 and 3.4 are primary test environments.

+ pip and setuptools

  * http://pypi.python.org/pypi/pip
  * http://pypi.python.org/pypi/setuptools

License
=======

  | Copyright (c) 2015-2018 Adam Karpierz
  |
  | Licensed under the MIT License
  | http://opensource.org/licenses/MIT
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <python@python.pl>
