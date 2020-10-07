.. _topics-overlays:

********
Overlays
********

An overlay is a collection of functions that provide an interface to command creation. An overlay allows configuration files to specify commands in a generic way. When the file is loaded, an overlay may be specified which Script Tease uses to generate commands that are specific to a given operating system.

There are currently four (5) general and re-usable overlays:

- common
- django
- mysql
- pgsql
- posix

And two (2) overlays that are specific to operating systems:

- centos
- ubuntu

The examples that follow instantiate command instances from an INI file. Each example is shown with the defaults. All commands support a number of :ref:`topics-configuration-common-parameters`.

.. include:: _includes/overlays.rst
