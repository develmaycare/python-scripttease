# Testing

## Set Up for Testing

Install requirements:

``pip install tests/requirements.pip``

## Running Tests

Run all tests with coverage:

``make tests``

Run a specific test:

``python -m pytest tests/units/path/to/test.py``

Example:

``python -m pytest tests/units/shortcuts/test_shortcuts.py``

To allow output from print statements within a test method, add the ``-s`` switch:

``python -m pytest -s tests/units/path/to/test.py``

> Tip: Add ``-v`` to list the tests with PASS/FAIL.

## Reference

- [coverage](https://coverage.readthedocs.io/en/v4.5.x/)
- [pytest](https://pytest.org)
