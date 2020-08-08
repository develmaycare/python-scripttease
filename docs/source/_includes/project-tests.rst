Coverage Requirements
---------------------

100% coverage is required for the ``master`` branch.

See `current coverage report <coverage/index.html>`_.

.. csv-table:: Lines of Code
    :file: ../_data/cloc.csv

Set Up for Testing
------------------

Install requirements:

.. code-block:: bash

    pip install tests/requirements.pip

Running Tests
.............

.. tip::
    You may use the ``tests`` target of the ``Makefile`` to run tests with coverage:

    ``make tests;``

To run unit tests:

.. code-block:: bash

    python -m pytest;

Run a specific test:

.. code-block:: bash

    python -m pytest tests/units/path/to/test.py

To allow output from print statements within a test method, add the ``-s`` switch:

.. code-block:: bash

    python -m pytest -s tests/units/path/to/test.py

Reference
---------

- `coverage <https://coverage.readthedocs.io/en/v4.5.x/>`_
- `pytest <https://pytest.org>`_
