#! /usr/bin/env python

# Imports

from collections import OrderedDict
import inspect
import sys

# Set path before importing overlays.
sys.path.append("../")

# Import overlays
from scripttease.library.overlays.common import COMMON_MAPPINGS
from scripttease.library.overlays.centos import MAPPINGS as CENTOS_MAPPINGS
from scripttease.library.overlays.django import DJANGO_MAPPINGS
from scripttease.library.overlays.pgsql import PGSQL_MAPPINGS
from scripttease.library.overlays.posix import POSIX_MAPPINGS
from scripttease.library.overlays.ubuntu import MAPPINGS as UBUNTU_MAPPINGS

# Functions


# https://stackoverflow.com/a/52003056/241720
def get_signature(fn):
    params = inspect.signature(fn).parameters
    args = []
    kwargs = OrderedDict()
    for p in params.values():
        if p.default is p.empty:
            args.append(p.name)
        else:
            kwargs[p.name] = p.default
    return args, kwargs


def print_description(text):
    print(text)
    print("")


def print_heading(title):
    print(title)
    print("=" * len(title))
    print("")


def print_mapping(commands, excludes=None):
    keys = list(commands.keys())
    keys.sort()

    _excludes = excludes or dict()

    for key in keys:
        if key in _excludes:
            continue

        func = commands[key]

        docstring = func.__doc__
        if not docstring:
            continue

        print(key)
        print("-" * len(key))
        print("")
        for i in docstring.split("\n"):
            print(i.strip())
        # print("")

        print(".. code-block:: ini")
        print("")
        print("    [run %s command]" % key)

        args, kwargs = get_signature(func)

        line = list()
        for a in args:
            if a != "kwargs":
                line.append(a)

        print("    %s: %s" % (key, " ".join(line)))

        for option, value in kwargs.items():
            if value is True:
                _value = "yes"
            elif value is False:
                _value = "no"
            else:
                _value = value

            print("    %s: %s" % (option, value))

        print("")


# Overlay output.

print_heading("Common")
print_description("Common commands are available to all overlays.")
print_mapping(COMMON_MAPPINGS)

print_heading("Django")
print_description("Django commands are available to all overlays.")
print_mapping(DJANGO_MAPPINGS)

print_heading("Postgres")
print_description("Postgres commands.")
print_mapping(PGSQL_MAPPINGS)

print_heading("POSIX")
print_description("Posix commands form the basis of overlays for nix platforms.")
print_mapping(POSIX_MAPPINGS)

exclude_from_centos = COMMON_MAPPINGS.copy()
exclude_from_centos.update(DJANGO_MAPPINGS)
exclude_from_centos.update(PGSQL_MAPPINGS)
exclude_from_centos.update(POSIX_MAPPINGS)
print_heading("Cent OS")
print_description("The Cent OS overlay incorporates commands specific to that platform as well as commands from "
                  "common, Django, Postgres, and POSIX.")
print_mapping(CENTOS_MAPPINGS, excludes=exclude_from_centos)

exclude_from_ubuntu = COMMON_MAPPINGS.copy()
exclude_from_ubuntu.update(DJANGO_MAPPINGS)
exclude_from_ubuntu.update(PGSQL_MAPPINGS)
exclude_from_ubuntu.update(POSIX_MAPPINGS)
print_heading("Ubuntu")
print_description("The Ubuntu overlay incorporates commands specific to that platform as well as commands from "
                  "common, Django, Postgres, and POSIX.")
print_mapping(UBUNTU_MAPPINGS, excludes=exclude_from_ubuntu)
