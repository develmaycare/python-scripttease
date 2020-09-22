import pytest
from scripttease.library.overlays.pgsql import *


def test_pgsql_create():
    c = pgsql_create("testing", admin_pass="secret", template="mytemplate")
    s = c.get_statement()
    assert "createdb" in s
    assert "export PGPASSWORD=" in s
    assert "--host=" in s
    assert "--port=" in s
    assert "--username=" in s
    assert "--owner=" in s
    assert "--template=mytemplate" in s
    assert "testing" in s


def test_pgsql_exists():
    c = pgsql_exists("testing")
    s = c.get_statement()
    assert "psql" in s
    assert "pgsql_db_exists" in s


def test_pgsql_drop():
    c = pgsql_drop("testing")
    s = c.get_statement()
    assert "dropdb" in s
    assert "testing" in s


def test_pgsql_dump():
    c = pgsql_dump("testing")
    s = c.get_statement()
    assert "pg_dump" in s
    assert "--column-inserts" in s
    assert "--file=testing.sql" in s


def test_pgsql_exec():
    c = pgsql_exec("SELECT * FROM projects", database="testing")
    s = c.get_statement()
    assert "psql" in s
    assert "--dbname=testing" in s
    assert '-c "SELECT * FROM projects"' in s


def test_pgsql_user():
    c = pgsql_user("testing", password="secret")
    s = c.get_statement()
    assert "createuser" in s
    assert "-DRS" in s
    assert "testing" in s
    assert "ALTER USER testing" in s

    c = pgsql_user("testing", op="drop")
    s = c.get_statement()
    assert "dropuser" in s
    assert "testing" in s

    c = pgsql_user("testing", op="exists")
    s = c.get_statement()
    assert "SELECT 1 FROM pgsql_roles" in s

    with pytest.raises(NameError):
        pgsql_user("testing", op="nonexistent")
