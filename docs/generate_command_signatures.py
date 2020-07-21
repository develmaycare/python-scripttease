#! /usr/bin/env python

from collections import OrderedDict
import inspect
import sys

sys.path.append("../")

from script_tease.mappings import MAPPING


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


keys = list(MAPPING.keys())
keys.sort()

for key in keys:
    cls = MAPPING[key]

    print(key)
    print("." * len(key))
    print("")

    extra = cls.get_docs()
    if extra is not None:
        print(extra)
        print("")

    # if cls.__init__.__doc__:
    #     print(cls.__init__.__doc__)
    #     print("")

    print(".. code-block:: cfg")
    print("")

    if cls.__doc__:
        print("    [%s]" % cls.__doc__.strip().replace(".", "").lower())
    else:
        print("    [run a %s command]" % cls.__name__.lower())

    args, kwargs = get_signature(cls.__init__)

    line = list()
    for a in args:
        if a not in ("self", "kwargs"):
            line.append(a)

    print("    %s = %s" % (key, " ".join(line)))

    for option, value in kwargs.items():
        print("    %s = %s" % (option, value))

    print("")

