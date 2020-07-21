from scripttease.library.overlays.django import *


def test_django():
    c = django("check")
    assert "./manage.py check" in c.get_statement()

    c = django("collectstatic")
    assert "./manage.py collectstatic" in c.get_statement()

    c = django("migrate")
    assert "./manage.py migrate" in c.get_statement()

    c = django("custom", "arg1", "arg2", venv="python", settings="tenants.example.settings", quiet=True)
    s = c.get_statement()
    assert "./manage.py custom" in s
    assert "arg1" in s
    assert "arg2" in s
    assert "--settings=" in s
    assert "source python/bin/activate" in s
    assert "--quiet" in s


def test_django_check():
    c = django_check(venv="python")
    s = c.get_statement()
    assert "./manage.py check" in s
    assert "source python/bin/activate" in s


def test_django_collect_static():
    c = django_collect_static(venv="python")
    s = c.get_statement()
    assert "./manage.py collectstatic" in s
    assert "source python/bin/activate" in s


def test_django_dumpdata():
    c = django_dumpdata("projects")
    s = c.get_statement()
    assert "./manage.py dumpdata" in s
    assert "projects >" in s
    assert "--format=json" in s
    assert "--indent=4" in s
    assert "local/projects/fixtures/initial.json" in s


def test_django_loaddata():
    c = django_loaddata("projects")
    s = c.get_statement()
    print(s)
    assert "./manage.py loaddata" in s
    assert "local/projects/fixtures/initial.json" in s


def test_django_migrate():
    c = django_migrate(cd="/path/to/project/", venv="python")
    s = c.get_statement(cd=True)
    assert "./manage.py migrate" in s
    assert "source python/bin/activate" in s
    assert "cd /path/to/project/" in s
