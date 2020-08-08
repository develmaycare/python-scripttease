# Imports

from ..commands import Command

# Exports

__all__ = (
    "PGSQL_MAPPINGS",
    "pg_create_database",
    "pg_create_user",
    "pg_database_exists",
    "pg_drop_database",
    "pg_drop_user",
    "pg_dump_database",
    "psql",
)

# Functions


def _get_pgsql_command(name, host="localhost", password=None, port=5432, user="postgres"):
    """Get a postgres-related command using commonly required parameters.

    :param name: The name of the command.
    :type name: str

    :param host: The host name.
    :type host: str

    :param password: The password to use.
    :type password: str

    :param port: The TCP port number.
    :type port: int

    :param user: The user name that will be used to execute the command.

    :rtype: list[str]

    """
    a = list()

    if password:
        a.append('export PGPASSWORD="%s" &&' % password)

    a.append(name)

    a.append("--host=%s" % host)
    a.append("--port=%s" % port)
    a.append("--username=%s" % user)

    return a


def pg_create_database(name, admin_pass=None, admin_user="postgres", host="localhost", owner=None, port=5432,
                       template=None, **kwargs):
    """Create a PostgreSQL database.

    - name (str): The database name.
    - admin_pass (str): The password for the user with sufficient access privileges to execute the command.
    - admin_user (str): The name of the user with sufficient access privileges to execute the command.
    - host (str): The database host name or IP address.
    - owner (str): The owner (user/role name) of the new database.
    - port (int): The port number of the Postgres service running on the host.
    - template (str): The database template name to use, if any.

    """
    _owner = owner or admin_user

    # Postgres commands always run without sudo because the -U may be provided.
    kwargs['sudo'] = False

    # Assemble the command.
    base = _get_pgsql_command("createdb", host=host, password=admin_pass, port=port)
    base.append("--owner=%s" % _owner)

    if template is not None:
        base.append("--template=%s" % template)

    base.append(name)

    return Command(" ".join(base), **kwargs)


def pg_create_user(name, admin_pass=None, admin_user="postgres", host="localhost", password=None, port=5432, **kwargs):
    """Create a PostgreSQL user.

    - name (str): The user name.
    - admin_pass (str): The password for the user with sufficient access privileges to execute the command.
    - admin_user (str): The name of the user with sufficient access privileges to execute the command.
    - host (str): The database host name or IP address.
    - port (int): The port number of the Postgres service running on the host.

    """
    # Postgres commands always run without sudo because the -U may be provided.
    kwargs['sudo'] = False

    # Assemble the command.
    base = _get_pgsql_command("createuser", host=host, password=admin_pass, port=port)
    base.append("-DRS")
    base.append(name)

    if password is not None:
        base.append("&& psql -h %s -U %s" % (host, admin_user))
        base.append("-c \"ALTER USER %s WITH ENCRYPTED PASSWORD '%s';\"" % (name, password))

    return Command(" ".join(base), **kwargs)


def pg_database_exists(name, admin_pass=None, admin_user="postgres", host="localhost", port=5432, **kwargs):
    """Determine if a Postgres database exists.

    - name (str): The database name.
    - admin_pass (str): The password for the user with sufficient access privileges to execute the command.
    - admin_user (str): The name of the user with sufficient access privileges to execute the command.
    - host (str): The database host name or IP address.
    - owner (str): The owner (user/role name) of the new database.
    - port (int): The port number of the Postgres service running on the host.

    """
    # Postgres commands always run without sudo because the -U may be provided. However, sudo may be required for
    # file writing.
    # kwargs['sudo'] = False

    kwargs.setdefault("register", "%s_db_exists" % name)

    base = _get_pgsql_command("psql", host=host, password=admin_pass, port=port, user=admin_user)
    base.append(r"-lqt | cut -d \| -f 1 | grep -qw %s" % name)

    return Command(" ".join(base), **kwargs)


def pg_drop_database(name, admin_pass=None, admin_user="postgres", host="localhost", port=5432, **kwargs):
    """Remove a PostgreSQL database.

    - name (str): The database name.
    - admin_pass (str): The password for the user with sufficient access privileges to execute the command.
    - admin_user (str): The name of the user with sufficient access privileges to execute the command.
    - host (str): The database host name or IP address.
    - port (int): The port number of the Postgres service running on the host.

    """
    # Postgres commands always run without sudo because the -U may be provided.
    kwargs['sudo'] = False

    # Assemble the command.
    base = _get_pgsql_command("dropdb", host=host, password=admin_pass, port=port, user=admin_user)
    base.append(name)

    return  Command(" ".join(base), **kwargs)


def pg_drop_user(name, admin_pass=None, admin_user="postgres", host="localhost", port=5432, **kwargs):
    """Remove a Postgres user.

    - name (str): The user name.
    - admin_pass (str): The password for the user with sufficient access privileges to execute the command.
    - admin_user (str): The name of the user with sufficient access privileges to execute the command.
    - host (str): The database host name or IP address.
    - port (int): The port number of the Postgres service running on the host.

    """
    # Postgres commands always run without sudo because the -U may be provided.
    kwargs['sudo'] = False

    # Assemble the command.
    base = _get_pgsql_command("dropuser", host=host, password=admin_pass, port=port, user=admin_user)
    base.append(name)

    return Command(" ".join(base), **kwargs)


def pg_dump_database(name, admin_pass=None, admin_user="postgres", file_name=None, host="localhost", port=5432,
                     **kwargs):
    """Export a Postgres database.

    - name (str): The database name.
    - admin_pass (str): The password for the user with sufficient access privileges to execute the command.
    - admin_user (str): The name of the user with sufficient access privileges to execute the command.
    - file_name (str): The name/path of the export file. Defaults the database name plus ``.sql``.
    - host (str): The database host name or IP address.
    - port (int): The port number of the Postgres service running on the host.

    """
    _file_name = file_name or "%s.sql" % name

    # Postgres commands always run without sudo because the -U may be provided.
    kwargs['sudo'] = False

    # Assemble the command.
    base = _get_pgsql_command("pg_dump", host=host, password=admin_pass, port=port, user=admin_user)
    base.append("--column-inserts")
    base.append("--file=%s" % _file_name)
    base.append(name)

    return Command(" ".join(base), **kwargs)


def psql(sql, database="template1", host="localhost", password=None, port=5432, user="postgres", **kwargs):
    """Execute a psql command.

    - sql (str): The SQL to be executed.
    - database (str): The database name.
    - admin_pass (str): The password for the user with sufficient access privileges to execute the command.
    - admin_user (str): The name of the user with sufficient access privileges to execute the command.
    - host (str): The database host name or IP address.
    - port (int): The port number of the Postgres service running on the host.

    """
    # Postgres commands always run without sudo because the -U may be provided.
    kwargs['sudo'] = False

    # Assemble the command.
    base = _get_pgsql_command("psql", host=host, password=password, port=port, user=user)
    base.append("--dbname=%s" % database)
    base.append('-c "%s"' % sql)

    return Command(" ".join(base), **kwargs)


PGSQL_MAPPINGS = {
    'pg.client': psql,
    'pg.createdatabase': pg_create_database,
    'pg.createdb': pg_create_database,
    'pg.createuser': pg_create_user,
    'pg.database': pg_create_database,
    'pg.database_exists': pg_database_exists,
    'pg.db': pg_create_database,
    'pg.dropdatabase': pg_drop_database,
    'pg.dropdb': pg_drop_database,
    'pg.dropuser': pg_drop_user,
    'pg.dump': pg_dump_database,
    'pg.dumpdb': pg_dump_database,
    'pg.exists': pg_database_exists,
    'pg.user': pg_create_user,
    'psql': psql,
}
