# Imports

from .centos import centos
from .django import django
from .messages import messages
from .mysql import mysql
from .pgsql import pgsql
from .posix import posix
from .python import python
from .ubuntu import ubuntu

# Exports

# Functions


def merge(first: dict, *others) -> dict:
    """Merge all other dictionaries into the first.

    :param first: The first dictionary.
    :type first: dict

    :param others: A list of other dictionaries to be merged.

    """
    for d in others:
        first = merge_dictionaries(first, d)

    return first


def merge_dictionaries(first: dict, second: dict) -> dict:
    """Merge the second dictionary into the first.

    :param first: The first dictionary.
    :type first: dict

    :param second: The second dictionary.
    :type second: dict

    :rtype: dict

    """
    for key, values in second.items():
        first[key] = values

    return first

# Mappings


MAPPINGS = {
    'centos': merge(centos, django, messages, mysql, pgsql, posix, py),
    'ubuntu': merge(ubuntu, django, messages, mysql, pgsql, posix, python),
}
