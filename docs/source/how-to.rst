.. _how-to:

******
How To
******

Create a New Command Overlay
============================

:ref:`topics-overlays` are used to define the commands supported by a given application, service, or operating system. Commands are defined as a function.

1) Define a Module
------------------

The first step is to create a new module in which functions will be defined.

.. code-block:: python

    # module_name.py
    from ..commands import Command

For overlays that represent an operating system, the ``command_exists()`` function is required:

.. code-block:: python

    def command_exists(name):
        return name in MAPPINGS


2) Define Command Function
--------------------------

The purpose of each function is to provide an interface for instantiating a :py:class`scripttease.library.commands.base.Command` instance. The example below is taken from the ``posix`` module.

.. code-block:: python

    # module_name.py
    # ...

    def mkdir(path, mode=None, recursive=True, **kwargs):
        """Create a directory.

        - path (str): The path to be created.
        - mode (int | str): The access permissions of the new directory.
        - recursive (bool): Create all directories along the path.

        """
        kwargs.setdefault("comment", "create directory %s" % path)

        statement = ["mkdir"]
        if mode is not None:
            statement.append("-m %s" % mode)

        if recursive:
            statement.append("-p")

        statement.append(path)

        return Command(" ".join(statement), **kwargs)

The arguments and any specific keyword arguments are automatically used by the parser, but also serve as a simple interface for programmatic use.

Each function *must* also accept ``**kwargs`` and should set a default for ``comment`` as above.

3) Add Functions to the Mapping
-------------------------------

The final step adds the function to the mapping. This makes it available to the command factory.

.. code-block:: python

    # module_name.py
    # ...

    MAPPINGS = {
        'mkdir': mkdir,
    }

For overlays that represent an operating system, ``MAPPINGS`` is required -- in addition to ``command_exists()`` above. For commands that are specific to service or application, the name of the dictionary may be anything that is appropriate. For example, ``DJANGO_MAPPINGS``.

Additionally, for an operating system overlay, you may wish to import other mappings and incorporate them into ``MAPPINGS``.

.. code-block:: python

    # module_name.py
    from ..commands import Command
    from .common import COMMON_MAPPINGS
    from .django import DJANGO_MAPPINGS
    from .pgsql import PGSQL_MAPPINGS

    MAPPINGS = {
        # ...
    }

    MAPPINGS.update(COMMON_MAPPINGS)
    MAPPINGS.update(DJANGO_MAPPINGS)
    MAPPINGS.update(PGSQL_MAPPINGS)

Export Commands as a Script
===========================

.. code-block:: python

    config = Config("commands.ini")
    if not config.load():
        print("Bummer!")
        exit()

    script = config.as_script()
    print(script)
