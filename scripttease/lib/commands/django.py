"""
[run django checks]
django: check

[export fixtures]
django: dump lookups.Category

[import fixtures]
django: load lookups.Category

[migrate the database]
django: migrate

[collect static files]
django: static

[create super user (ad hoc command)]
django: createsuperuser root

"""
from .base import EXCLUDED_KWARGS, Command


def django(management_command, *args, excluded_kwargs=None, **kwargs):
    # The excluded parameters (filtered below) may vary based on implementation. We do, however, need a default.
    excluded_kwargs = excluded_kwargs or EXCLUDED_KWARGS

    # Django's management commands can have a number of options. We need to filter out internal parameters so that these
    # are not used as options for the management command.
    _kwargs = dict()
    for key in excluded_kwargs:
        if key in kwargs:
            _kwargs[key] = kwargs.pop(key)

    if 'comment' not in _kwargs:
        _kwargs['comment'] = "run %s django management command" % management_command

    a = list()
    a.append("./manage.py %s" % management_command)
    for key, value in kwargs.items():
        key = key.replace("_", "-")
        if type(value) is bool and value is True:
            a.append("--%s" % key)
        elif type(value) is str:
            a.append('--%s="%s"' % (key, value))
        else:
            a.append('--%s=%s' % (key, value))

    _args = list(args)
    if len(_args) > 0:
        a.append(" ".join(_args))

    statement = " ".join(a)

    return Command(statement, **_kwargs)


def django_check(**kwargs):
    kwargs.setdefault("comment", "run django checks")
    kwargs.setdefault("register", "django_checks_out")
    return django("check", **kwargs)


def django_dump(target, path=None, **kwargs):
    kwargs.setdefault("comment", "dump app/model data")
    kwargs.setdefault("format", "json")
    kwargs.setdefault("indent", 4)

    if path is None:
        path = "../deploy/fixtures/%s.%s" % (target, kwargs['format'])

    return django("dumpdata", target, "> %s" % path, **kwargs)


def django_load(target, path=None, **kwargs):
    kwargs.setdefault("comment", "load app/model data")
    input_format = kwargs.pop("format", "json")
    if path is None:
        path = "../deploy/fixtures/%s.%s" % (target, input_format)

    return django("loaddata", path, **kwargs)


def django_migrate(**kwargs):
    kwargs.setdefault("comment", "apply database migrations")
    return django("migrate", **kwargs)


def django_static(**kwargs):
    kwargs.setdefault("comment", "collect static files")
    kwargs.setdefault("noinput", True)
    return django("collectstatic", **kwargs)
