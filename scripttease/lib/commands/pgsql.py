"""

"""
from ...constants import EXCLUDED_KWARGS
from ...exceptions import InvalidInput
from .base import Command


__all__ = (
    "PGSQL_MAPPINGS",
    "pgsql_create",
    "pgsql_drop",
    "pgsql_dump",
    "pgsql_exists",
    "pgsql_load",
    "pgsql_user",
)


def pgsql(command, *args, host="localhost", excluded_kwargs=None, password=None, port=5432, user="postgres", **kwargs):
    # The excluded parameters (filtered below) may vary based on implementation. We do, however, need a default.
    excluded_kwargs = excluded_kwargs or EXCLUDED_KWARGS

    # if 'comment' not in kwargs:
    #     kwargs['comment'] = "run %s postgres command" % command

    # Allow additional command line switches to pass through?
    _kwargs = dict()
    for key in excluded_kwargs:
        if key in kwargs:
            _kwargs[key] = kwargs.pop(key)

    # Postgres commands always run without sudo because the -U may be provided.
    _kwargs['sudo'] = False

    a = list()

    if password is not None:
        a.append('export PGPASSWORD="%s" &&' % password)

    a.append(command)
    a.append("-U %s --host=%s --port=%s" % (user, host, port))
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


def pgsql_create(database, owner=None, template=None, **kwargs):
    kwargs.setdefault("comment", "create %s postgres database" % database)

    if owner is not None:
        kwargs['owner'] = owner

    if template is not None:
        kwargs['template'] = template

    # psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '<your db name>'" | grep -q 1 | psql -U postgres -c "CREATE DATABASE <your db name>"
    # first = pgsql("psql", **kwargs)
    #
    # first_query = "SELECT 1 FROM pg_database WHERE datname = '%s'" % database
    # first_statement = '%s -tc "%s" | grep -q 1' % (first.statement, first_query)
    #
    # kwargs_without_password = kwargs.copy()
    # if 'password' in kwargs_without_password:
    #     kwargs_without_password.pop("password")
    #
    # second = pgsql("psql", **kwargs_without_password)
    # second_statement = '%s -c "CREATE DATABASE %s"' % (second.statement, database)
    #
    # final_statement = "%s | %s" % (first_statement, second_statement)
    # return Command(final_statement, **kwargs)

    return pgsql("createdb", database, **kwargs)


def pgsql_drop(database, **kwargs):
    kwargs.setdefault("comment", "drop %s postgres database" % database)

    return pgsql("dropdb", database, **kwargs)


def pgsql_dump(database, path=None, **kwargs):
    kwargs.setdefault("comment", "dump postgres database")
    kwargs.setdefault("column_inserts", True)

    if path is None:
        path = "%s.sql" % database

    kwargs['dbname'] = database
    kwargs['file'] = path

    return pgsql("pg_dump", **kwargs)


def pgsql_exists(database, **kwargs):
    kwargs.setdefault("comment", "determine if %s postgres database exists" % database)
    kwargs.setdefault("register", "%s_exists" % database)

    command = pgsql("psql", **kwargs)
    command.statement += r" -lqt | cut -d \| -f 1 | grep -qw %s" % database

    return command


def pgsql_load(database, path, **kwargs):
    kwargs.setdefault("comment", "load data into a postgres database")

    kwargs['dbname'] = database
    kwargs['file'] = path

    return pgsql("psql", **kwargs)


def pgsql_user(name, admin_pass=None, admin_user="postgres", op="create", password=None, **kwargs):
    if op == "create":
        kwargs.setdefault("comment", "create %s postgres user" % name)

        command = pgsql("createuser", "-DRS %s" % name, password=admin_pass, user=admin_user, **kwargs)

        if password is not None:
            extra = pgsql("psql", password=admin_pass, user=admin_user, **kwargs)
            command.statement += " && " + extra.statement
            command.statement += " -c \"ALTER USER %s WITH ENCRYPTED PASSWORD '%s';\"" % (name, password)

        return command
    elif op == "drop":
        kwargs.setdefault("comment", "remove %s postgres user" % name)

        return pgsql("dropuser", name, password=admin_pass, user=admin_user, **kwargs)
    elif op == "exists":
        kwargs.setdefault("comment", "determine if %s postgres user exists" % name)
        kwargs.setdefault("register", "pgsql_use_exists")

        command = pgsql("psql", password=admin_pass, user=admin_user, **kwargs)

        sql = "SELECT 1 FROM pgsql_roles WHERE rolname='%s'" % name

        command.statement += ' -c "%s"' % sql

        return command
    else:
        raise InvalidInput("Unrecognized or unsupported Postgres user operation: %s" % op)


PGSQL_MAPPINGS = {
    'pgsql.create': pgsql_create,
    'pgsql.drop': pgsql_drop,
    'pgsql.dump': pgsql_dump,
    'pgsql.exists': pgsql_exists,
    # 'pgsql.sql': pgsql_exec,
    'pgsql.user': pgsql_user,
}
