.. _commands:

********
Commands
********

.. code-block:: text

    usage: tease [-h] [-c] [-C= VARIABLES] [-d] [-D] [-f= FILTERS] [-O= OPTIONS] [-s] [-T= TEMPLATE_LOCATIONS] [-w= OUTPUT_FILE] [-V= VARIABLES_FILE]
                 [-v] [--version]
                 [path]

    positional arguments:
      path                  The path to the configuration file.

    optional arguments:
      -h, --help            show this help message and exit
      -c, --color           Enable code highlighting for terminal output.
      -C= VARIABLES, --context= VARIABLES
                            Context variables for use in pre-parsing the config and templates. In the form of: name:value
      -d, --docs            Output documentation instead of code.
      -D, --debug           Enable debug output.
      -f= FILTERS, --filter= FILTERS
                            Filter the commands in the form of: attribute:value
      -O= OPTIONS, --option= OPTIONS
                            Common command options in the form of: name:value
      -s, --script          Output commands as a script.
      -T= TEMPLATE_LOCATIONS, --template-path= TEMPLATE_LOCATIONS
                            The location of template files that may be used with the template command.
      -w= OUTPUT_FILE, --write= OUTPUT_FILE
                            Write the output to disk.
      -V= VARIABLES_FILE, --variables-file= VARIABLES_FILE
                            Load variables from a file.
      -v                    Show version number and exit.
      --version             Show verbose version information and exit.

    NOTES

    This command is used to parse configuration files and output the commands.

Using the Tease Command
=======================

The ``tease`` command may be used to parse a configuration file, providing additional utilities for working with commands.

The ``path`` argument defaults to ``commands.ini``.

Context Variables May be Provided on the Command Line
-----------------------------------------------------

To supply context variables on the command line:

.. code-block:: bash

    tease -C domain_name:example.com -C domain_tld:example_com

Loading Context Variables from a File
-------------------------------------

Context variables may be loaded from a file:

.. code-block:: ini

    [domain]
    name = example.com
    tld = example_com

The variables above are available as ``section_key``. For example, ``domain_name`` is ``example.com``.

.. code-block:: bash

    tease -V variables.ini

Setting Common Options for All Commands
---------------------------------------

Rather than include a common parameter in the configuration file, it is possible to specify a common option on the command line.

.. code-block:: bash

    tease -O sudo:yes

The Difference Between Variables and Options
--------------------------------------------

Variables are used to pre-process configuration files as templates, while common options are passed to *all* command instances.
