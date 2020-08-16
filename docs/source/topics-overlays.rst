.. _topics-overlays:

*******
Overlay
*******

An overlay is a collection of functions that provide an interface to command creation.

There are currently four (4) general and re-usable overlays:

- common
- django
- pgsql
- posix

And two (2) overlays that are specific to operating systems:

- centos
- ubuntu

The examples that follow instantiate command instances from an INI file. Each example is shown with the defaults. All commands support a number of :ref:`topics-configuration-common-parameters`.

.. include:: _includes/overlays.rst
