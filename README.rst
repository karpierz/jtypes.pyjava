jtypes.pyjava
=============

A Python to Java bridge.

Overview
========

| |package_bold| is a bridge allowing to use Java classes in regular Python code.

`PyPI record`_.

`Documentation`_.

| |package_bold| is an almost fully compliant implementation of Remi Rampin's
  **PyJava** package by reimplementing whole its functionality in a clean Python
  instead of C.
| |package_bold| package is closely based on the `jvm`_ and `jni`_ Python packages.

About PyJava:
-------------

Borrowed from the `original website`_:

| **PyJava** is a bridge allowing to use Java classes in regular Python code.
| It is similar to `JPype <http://jpype.sourceforge.net/>`__.

It is a C extension that uses JNI to access a Java virtual machine,
meaning that it can be used anywhere Python is available. It is not
a different interpreter like `Jython <https://www.jython.org/>`__ and does
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

Prerequisites:

+ Python 3.9 or higher

  * https://www.python.org/
  * Java 11 is a primary test environment.

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

  .. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

Visit `Development page`_.

Installation from sources:

clone the sources:

  .. parsed-literal::

    git clone |respository| |package|

and run:

  .. parsed-literal::

    python -m pip install ./|package|

or on development mode:

  .. parsed-literal::

    python -m pip install --editable ./|package|

License
=======

  | |copyright|
  | Licensed under the MIT License
  | https://opensource.org/license/mit
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: jtypes.pyjava
.. |package_bold| replace:: **jtypes.pyjava**
.. |copyright| replace:: Copyright (c) 2016-2024 Adam Karpierz
.. |respository| replace:: https://github.com/karpierz/jtypes.pyjava.git
.. _Development page: https://github.com/karpierz/jtypes.pyjava
.. _PyPI record: https://pypi.org/project/jtypes.pyjava/
.. _Documentation: https://jtypespyjava.readthedocs.io/
.. _jvm: https://pypi.org/project/jvm/
.. _jni: https://pypi.org/project/jni/
.. _original website: https://github.com/remram44/pyjava/blob/master/README.md
