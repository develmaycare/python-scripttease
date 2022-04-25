# Imports

from ...constants import EXCLUDED_KWARGS
from ...exceptions import InvalidInput
from .base import Command

# Exports

__all__ = (
    "MYSQL_MAPPINGS",
    "mysql_create",
    "mysql_dump",
    "mysql_exists",
    "mysql_load",
    "mysql_user",
)


def mysql(command, *args, host="localhost", excluded_kwargs=None, password=None, port=3306, user="root", **kwargs):
    # The excluded parameters (filtered below) may vary based on implementation. We do, however, need a default.
    excluded_kwargs = excluded_kwargs or EXCLUDED_KWARGS

    # if 'comment' not in kwargs:
    #     kwargs['comment'] = "run %s mysql command" % command

    # Allow additional command line switches to pass through?
    # Django's management commands can have a number of options. We need to filter out internal parameters so that these
    # are not used as options for the management command.
    _kwargs = dict()
    for key in excluded_kwargs:
        if key in kwargs:
            _kwargs[key] = kwargs.pop(key)

    # MySQL commands always run without sudo because the --user may be provided.
    _kwargs['sudo'] = False

    a = list()

    a.append(command)
    a.append("--user %s --host=%s --port=%s" % (user, host, port))
    
    if password:
        a.append('--password="%s"' % password)
    
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


def mysql_create(database, owner=None, **kwargs):
    kwargs.setdefault("comment", "create mysql database")

    command = mysql("mysqladmin create", database, **kwargs)
    
    if owner is not None:
        grant = mysql_grant(owner, database=database, **kwargs)
        command.statement += " && " + grant.statement
        
    return command


def mysql_drop(database, **kwargs):
    kwargs.setdefault("comment", "drop %s mysql database" % database)

    return mysql("mysqladmin drop", database, **kwargs)


def mysql_dump(database, path=None, **kwargs):
    kwargs.setdefault("comment", "dump mysql database")
    kwargs.setdefault("complete_inserts", True)

    if path is None:
        path = "%s.sql" % database

    return mysql("mysqldump", database, "> %s" % path, **kwargs)


def mysql_exists(database, **kwargs):
    kwargs.setdefault("comment", "determine if %s mysql database exists" % database)
    kwargs.setdefault("register", "%s_exists" % database)

    command = mysql("mysql", **kwargs)
    
    sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '%s'" % database
    
    command.statement += '--execute="%s"' % sql
    
    return command


def mysql_grant(to, database=None, privileges="ALL", **kwargs):
    """Grant privileges to a user.

    - to (str): The user name to which privileges are granted.
    - database (str): The database name.
    - host (str): The database host name or IP address.
    - password (str): The password for the user with sufficient access privileges to execute the command.
    - port (int): The TCP port number of the MySQL service running on the host.
    - privileges (str): The privileges to be granted.
    - user (str): The name of the user with sufficient access privileges to execute the command.

    """
    kwargs.setdefault("comment", "grant mysql privileges to %s" % to)

    host = kwargs.get("host", "localhost")

    command = mysql("mysql", **kwargs)

    # See https://dev.mysql.com/doc/refman/5.7/en/grant.html
    _database = database or "*"
    sql = "GRANT %(privileges)s ON %(database)s.* TO '%(user)s'@'%(host)s'" % {
        'database': _database,
        'host': host,
        'privileges': privileges,
        'user': to,
    }
    command.statement += ' --execute="%s"' % sql

    return command


def mysql_load(database, path, **kwargs):
    kwargs.setdefault("comment", "load data into a mysql database")

    return mysql("psql", database, "< %s" % path, **kwargs)


def mysql_user(name, admin_pass=None, admin_user="root", op="create", password=None, **kwargs):
    host = kwargs.get("host", "localhost")

    if op == "create":
        kwargs.setdefault("comment", "create %s mysql user" % name)

        command = mysql("mysql", password=admin_pass, user=admin_user, **kwargs)

        sql = "CREATE USER IF NOT EXISTS '%s'@'%s'" % (name, host)
        if password is not None:
            sql += " IDENTIFIED BY PASSWORD('%s')" % password

        command.statement += ' --execute="%s"' % sql

        return command
    elif op == "drop":
        kwargs.setdefault("comment", "remove %s mysql user" % name)

        command = mysql("mysql", password=admin_pass, user=admin_user, **kwargs)

        sql = "DROP USER IF EXISTS '%s'@'%s'" % (name, host)

        command.statement += ' --execute="%s"' % sql

        return command
    elif op == "exists":
        kwargs.setdefault("comment", "determine if %s mysql user exists" % name)
        kwargs.setdefault("register", "mysql_use_exists")

        command = mysql("mysql", password=admin_pass, user=admin_user, **kwargs)

        sql = "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '%s')" % name

        command.statement += ' --execute "%s"' % sql

        return command
    else:
        raise InvalidInput("Unrecognized or unsupported MySQL user operation: %s" % op)


MYSQL_MAPPINGS = {
    'mysql.create': mysql_create,
    'mysql.drop': mysql_drop,
    'mysql.dump': mysql_dump,
    'mysql.exists': mysql_exists,
    'mysql.grant': mysql_grant,
    # 'mysql.sql': mysql_exec,
    'mysql.user': mysql_user,
}
