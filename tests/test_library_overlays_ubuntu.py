import pytest
from scripttease.library.commands.templates import Template
from scripttease.library.overlays.ubuntu import *


def test_apache():
    c = apache("reload")
    assert "service apache2 reload" in c.get_statement()

    c = apache("restart")
    assert "service apache2 restart" in c.get_statement()

    c = apache("start")
    assert "service apache2 start" in c.get_statement()

    c = apache("stop")
    assert "service apache2 stop" in c.get_statement()

    c = apache("test")
    assert "apachectl configtest" in c.get_statement()

    with pytest.raises(NameError):
        apache("nonexistent")


def test_apache_disable_module():
    c = apache_disable_module("mod_ssl")
    assert "a2dismod mod_ssl" in c.get_statement()


def test_apache_disable_site():
    c = apache_disable_site("default")
    assert "a2dissite default" in c.get_statement()


def test_apache_enable_module():
    c = apache_enable_module("mod_wsgi")
    assert "a2enmod mod_wsgi" in c.get_statement()


def test_apache_enable_site():
    c = apache_enable_site("example.com")
    assert "a2ensite example.com" in c.get_statement()


def test_service_reload():
    c = service_reload("postfix")
    assert "service postfix reload" in c.get_statement()


def test_service_restart():
    c = service_restart("postfix")
    assert "service postfix restart" in c.get_statement()


def test_service_start():
    c = service_start("postfix")
    assert "service postfix start" in c.get_statement()


def test_service_stop():
    c = service_stop("postfix")
    assert "service postfix stop" in c.get_statement()


def test_system():
    c = system("reboot")
    assert "reboot" in c.get_statement()

    c = system("update")
    assert "apt-get update -y" in c.get_statement()

    c = system("upgrade")
    assert "apt-get upgrade -y" in c.get_statement()

    with pytest.raises(NameError):
        system("nonexistent")


def test_system_install():
    c = system_install("vim")
    assert "apt-get install -y vim" in c.get_statement()


def test_system_uninstall():
    c = system_uninstall("lftp")
    assert "apt-get uninstall -y lftp" in c.get_statement()


def test_template():
    t = template("/path/to/source.txt", "/path/to/target.txt")
    assert isinstance(t, Template)
