.. _introduction:

************
Introduction
************

Script Tease is a library and command line tool for generating commands programmatically or using configuration files.

Concepts
========

Generating Commands
-------------------

Script Tease may be used in two (2) ways:

1. Using the library to programmatically define commands and export them as command line statements. See
   :ref:`developer-reference`.
2. Using the ``tease`` command to generate commands from a configuration file. See :ref:`configuration`.

Overlays
--------

An *overlay* is a set of command meta functions that define the capabilities of a specific operating system.

.. note::
    At present, the only fully defined overlay is for Ubuntu.
