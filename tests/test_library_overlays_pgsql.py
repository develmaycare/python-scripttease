from scripttease.library.overlays.pgsql import *


def test_pg_create_database():
    c = pg_create_database("testing", admin_pass="secret", template="mytemplate")
    s = c.get_statement()
    assert "createdb" in s
    assert "export PGPASSWORD=" in s
    assert "--host=" in s
    assert "--port=" in s
    assert "--username=" in s
    assert "--owner=" in s
    assert "--template=mytemplate" in s
    assert "testing" in s


def test_pg_create_user():
    c = pg_create_user("testing", password="secret")
    s = c.get_statement()
    assert "createuser" in s
    assert "-DRS" in s
    assert "testing" in s
    assert "ALTER USER testing" in s


def test_pg_database_exists():
    c = pg_database_exists("testing")
    s = c.get_statement()
    assert "psql" in s
    assert "testing_db_exists" in s


def test_pg_drop_database():
    c = pg_drop_database("testing")
    s = c.get_statement()
    assert "dropdb" in s
    assert "testing" in s


def test_pg_drop_user():
    c = pg_drop_user("testing")
    s = c.get_statement()
    assert "dropuser" in s
    assert "testing" in s


def test_pg_dump_database():
    c = pg_dump_database("testing")
    s = c.get_statement()
    assert "pg_dump" in s
    assert "--column-inserts" in s
    assert "--file=testing.sql" in s


def test_psql():
    c = psql("SELECT * FROM projects", database="testing")
    s = c.get_statement()
    assert "psql" in s
    assert "--dbname=testing" in s
    assert '-c "SELECT * FROM projects"' in s
