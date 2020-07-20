from ..commands import Command
from .common import python_pip, python_virtualenv
from .posix import file_append, file_copy, mkdir, move, perms, remove

name = "ubuntu"


def command_exists(name):
    return name in MAPPINGS


def apache_disable_module(name, **kwargs):
    kwargs.setdefault("comment", "disable %s apache module" % name)

    return Command("a2dismod %s" % name, **kwargs)


def apache_disable_site(name, **kwargs):
    kwargs.setdefault("comment", "disable %s apache site" % name)

    return Command("a2dissite %s" % name, **kwargs)


def apache_enable_module(name, **kwargs):
    kwargs.setdefault("comment", "enable %s apache module" % name)

    return Command("a2enmod %s" % name, **kwargs)


def apache_enable_site(name, **kwargs):
    kwargs.setdefault("comment", "enable %s apache module" % name)

    return Command("a2densite %s" % name, **kwargs)


def apache_reload(**kwargs):
    kwargs.setdefault("comment", "reload apache")
    kwargs.setdefault("register", "apache_reloaded")

    return Command("service apache2 reload", **kwargs)


def apache_restart(**kwargs):
    kwargs.setdefault("comment", "restart apache")
    kwargs.setdefault("register", "apache_restarted")

    return Command("service apache2 restart", **kwargs)


def apache_start(**kwargs):
    kwargs.setdefault("comment", "start apache")
    kwargs.setdefault("register", "apache_started")

    return Command("service apache2 start", **kwargs)


def apache_stop(**kwargs):
    kwargs.setdefault("comment", "stop apache")

    return Command("service apache2 stop", **kwargs)


def apache_test(**kwargs):
    kwargs.setdefault("comment", "check apache configuration")
    kwargs.setdefault("register", "apache_checks_out")

    return Command("apachectl configtest", **kwargs)


def service_reload(name, **kwargs):
    kwargs.setdefault("comment", "reload %s service" % name)
    kwargs.setdefault("register", "%s_reloaded" % name)

    return Command("service %s reload" % name, **kwargs)


def service_restart(name, **kwargs):
    kwargs.setdefault("comment", "restart %s service" % name)
    kwargs.setdefault("register", "%s_restarted" % name)

    return Command("service %s reload" % name, **kwargs)


def service_start(name, **kwargs):
    kwargs.setdefault("comment", "start %s service" % name)
    kwargs.setdefault("register", "%s_started" % name)

    return Command("service %s start" % name, **kwargs)


def service_stop(name, **kwargs):
    kwargs.setdefault("comment", "stop %s service" % name)
    kwargs.setdefault("register", "%s_stopped" % name)

    return Command("service %s stop" % name, **kwargs)


def system_install(name, **kwargs):
    kwargs.setdefault("comment", "install system package %s" % name)

    return Command("apt-get install -y %s" % name, **kwargs)


def system_reboot(**kwargs):
    kwargs.setdefault("comment", "reboot the system")

    return Command("reboot", **kwargs)


def system_uninstall(name, **kwargs):
    kwargs.setdefault("comment", "remove system package %s" % name)

    return Command("apt-get uninstall -y %s" % name, **kwargs)


def system_update(**kwargs):
    kwargs.setdefault("comment", "update system package info")

    return Command("apt-get update -y", **kwargs)


def system_upgrade(**kwargs):
    kwargs.setdefault("comment", "upgrade the system")

    return Command("apt-get upgrade -y", **kwargs)


MAPPINGS = {
    'apache.disable_module': apache_disable_module,
    'apache.disable_site': apache_disable_site,
    'apache.enable_module': apache_enable_module,
    'apache.enable_site': apache_enable_site,
    'apache.reload': apache_reload,
    'apache.restart': apache_restart,
    'apache.start': apache_start,
    'apache.stop': apache_stop,
    'apache.test': apache_test,
    'append': file_append,
    'copy': file_copy,
    'install': system_install,
    'mkdir': mkdir,
    'move': move,
    'perms': perms,
    'pip': python_pip,
    'reboot': system_reboot,
    'reload': service_reload,
    'remove': remove,
    'restart': service_restart,
    'start': service_start,
    'stop': service_stop,
    'update': system_update,
    'uninstall': system_uninstall,
    'upgrade': system_upgrade,
    'virtualenv': python_virtualenv,
}
