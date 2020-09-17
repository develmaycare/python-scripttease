import pytest
from scripttease.library.overlays.mysql import *


def test_mysql_create():
    c = mysql_create("testing", owner="bob", password="P455W0rD")
    s = c.get_statement()
    assert "mysqladmin" in s
    assert '--password="P455W0rD"' in s
    assert "--host=" in s
    assert "--port=" in s
    assert "create testing" in s
    assert '--execute="GRANT ALL ON testing.* TO \'bob\'@\'localhost\'"' in s


def test_mysql_drop():
    c = mysql_drop("testing")
    s = c.get_statement()
    assert "mysqladmin" in s
    assert "drop testing" in s


def test_mysql_dump():
    c = mysql_dump("testing", inserts=True)
    s = c.get_statement()
    assert "mysqldump" in s
    assert "--complete-inserts" in s
    assert "> testing.sql" in s


def test_mysql_exec():
    c = mysql_exec("SELECT * FROM projects", database="testing")
    s = c.get_statement()
    assert "mysql" in s
    assert "--execute=" in s
    assert '"SELECT * FROM projects"' in s


def test_mysql_exists():
    c = mysql_exists("testing")
    s = c.get_statement()
    assert "mysql" in s
    assert "mysql_database_exists" in s


def test_mysql_grant():
    c = mysql_grant("bob", database="testing")
    s = c.get_statement()
    assert "mysql" in s
    assert "GRANT" in s
    assert "testing.*" in s
    assert "'bob'@'localhost'" in s


def test_mysql_user():
    c = mysql_user("bob", passwd="secret")
    s = c.get_statement()
    assert "mysql" in s
    assert "CREATE USER IF NOT EXISTS" in s
    assert "'bob'@'localhost'" in s
    assert "IDENTIFIED BY PASSWORD('secret')" in s

    c = mysql_user("bob", op="drop", passwd="secret")
    s = c.get_statement()
    assert "mysql" in s
    assert "DROP USER IF EXISTS" in s
    assert "'bob'@'localhost'" in s

    c = mysql_user("bob", op="exists", passwd="secret")
    s = c.get_statement()
    assert "mysql" in s
    assert "mysql_user_exists" in s
    assert "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = 'bob')" in s

    with pytest.raises(NameError):
        mysql_user("bob", op="nonexistent")
