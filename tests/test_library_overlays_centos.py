import pytest
from scripttease.library.commands.templates import Template
from scripttease.library.overlays.centos import *


def test_apache():
    c = apache("reload")
    assert "apachectl –k reload" in c.get_statement()

    c = apache("restart")
    assert "apachectl –k restart" in c.get_statement()

    c = apache("start")
    assert "apachectl –k start" in c.get_statement()

    c = apache("stop")
    assert "apachectl –k stop" in c.get_statement()

    c = apache("test")
    assert "apachectl configtest" in c.get_statement()

    with pytest.raises(NameError):
        apache("nonexistent")


def test_command_exists():
    assert command_exists("apache") is True
    assert command_exists("nonexistent") is False


def test_service_reload():
    c = service_reload("postfix")
    assert "systemctl reload postfix" in c.get_statement()


def test_service_restart():
    c = service_restart("postfix")
    assert "systemctl restart postfix" in c.get_statement()


def test_service_start():
    c = service_start("postfix")
    assert "systemctl start postfix" in c.get_statement()


def test_service_stop():
    c = service_stop("postfix")
    assert "systemctl stop postfix" in c.get_statement()


def test_system():
    c = system("reboot")
    assert "reboot" in c.get_statement()

    c = system("update")
    assert "yum check-update" in c.get_statement()

    c = system("upgrade")
    assert "yum update -y" in c.get_statement()

    with pytest.raises(NameError):
        system("nonexistent")


def test_system_install():
    c = system_install("vim")
    assert "yum install -y vim" in c.get_statement()


def test_system_uninstall():
    c = system_uninstall("lftp")
    assert "yum remove -y lftp" in c.get_statement()


def test_template():
    t = template("/path/to/source.txt", "/path/to/target.txt")
    assert isinstance(t, Template)


def test_user():
    statement = user("deploy", groups="sudo", home="/path/to/deploy/root").get_statement()
    assert "adduser deploy" in statement
    assert "--home" in statement
    assert "gpasswd -a deploy sudo" in statement

    statement = user("deploy", op="remove").get_statement()
    assert "userdel -r deploy" in statement

    with pytest.raises(NameError):
        user("deploy", op="unsupported")
