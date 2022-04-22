from .base import Command


def php_module(name, **kwargs):
    statement = "phpenmod %s" % name

    return Command(statement, **kwargs)


PHP_MAPPINGS = {
    'php.module': php_module,
}
