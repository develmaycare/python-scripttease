.. _introduction:

************
Introduction
************

Overview
========

Script Tease is a library and command line tool for generating commands programmatically or (especially) using configuration files.

The primary focus (and limit) is to convert plain text instructions into valid command line statements for a given platform (see `Overlays`_). It does *not* provide support for executing those statements.

Concepts
========

Generating Commands
-------------------

Script Tease may be used in two (2) ways:

1. Using the library to programmatically define commands and export them as command line statements. See :ref:`developer-reference`.
2. Using the ``tease`` command to generate commands from a configuration file. See :ref:`topics-configuration`.

Overlays
--------

An *overlay* is a set of command meta functions that define the capabilities of a specific operating system.

.. note::
    At present, the only fully defined operating system overlays are for Cent OS and Ubuntu.

See :ref:`topics-overlays`.

Terms and Definitions
=====================

command
    When used in Script Tease documentation, this is a command instance which contains the properties and parameters for a command line statement.

statement
    A specific statement (string) to be executed. A *statement* is contained within a *command*.

License
=======

Script Tease is released under the BSD 3 clause license.
