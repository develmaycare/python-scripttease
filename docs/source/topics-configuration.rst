.. _topics-configuration:

*************
Configuration
*************

Generating Commands From a File
===============================

The :py:class:`scripttease.parsers.ini.Config` class may instantiate commands by loading a configuration file.

.. note::
    Additional formats such as JSON or YAML may be supported in the future.

An example file:

.. code-block:: ini

    [install apache]
    install: apache2

    [create the web site directory]
    mkdir: /var/www/domains/example_com/www
    recursive: yes

    [set permissions on the website directory]
    perms: /var/www/domains/example_com/www
    group: www-data
    mode: 775
    owner: www-data

Notes regarding this format:

- This is the standard format for Python's ConfigParser. If you prefer, you may use ``=`` instead of ``:``.
- The first part of each command is the INI section and is used as the default comment.
- The command name *must* be the *first* option in the section.
- The arguments for the command appear as the value of the first option in the section. Arguments are separated by a
  space.
- Arguments that should be treated as a single value should be enclosed in double quotes.
- ``yes`` and ``no`` are interpreted as boolean values.
- List values, where required, are separated by commas.

.. _topics-configuration-common-parameters:

Common Parameters
-----------------

All commands support the following common parameters:

- ``comment``: A comment regarding the command.
- ``condition``: A condition for execution. For example, ``! -f /path/to/some/file.txt``
- ``cd``: The path from which a command should be executed.
- ``environments``: A string or list of comma-separated strings indicating the operational environments in which the command runs. This is *not* used by default, but may be used to programmatically filter commands for a specific environment. For example, development versus live.
- ``prefix``: A statement to be added prior to executing the command.
- ``register``: A variable name to which the the success or failure (exit code) of the statement is captured.
- ``shell``: The shell used to run the commands. For example, ``/bin/bash``. This is generally not important, but can be a problem when attempting to execute some commands (such as Django management commands).
- ``stop``: ``True`` indicates no other commands should be executed if the given command fails.
- ``sudo``: ``True`` indicates the command should be automatically prefixed with ``sudo``. If provided as a string, the command is also prefixed with a specific user name.
- ``tags``: A list of tags used to classify the command.

Defining an "Itemized" Command
------------------------------

Certain command definitions may be repeated by defining a list of items.

Example of an "itemized" command:

.. code-block:: ini

    [touch a bunch of files]
    touch = /var/www/domains/example_com/www/$item
    items = index.html, assets/index.html, content/index.html

.. note::
    Command itemization may vary with the command type.

Pre-Parsing Command Files as Templates
======================================

Configuration file may be pre-processed as a Jinja2 template by providing a context dictionary:

.. code-block:: ini

    [install apache]
    install: apache

    [create the website directory]
    mkdir: /var/www/domains/{{ domain_tld }}/www
    recursive: yes

    [set permissions on the website directory]
    perms: /var/www/domains/{{ domain_tld }}/www
    group: www-data
    mode: 775
    owner: www-data

Then with a config instance:

.. code-block:: python

    context = {
        'domain_tld': "example_com",
    }

    config = Config("commands.ini", context=context)
    config.load()

    for command in config.get_commands():
        print(command.get_statement(cd=True))
        print("")
