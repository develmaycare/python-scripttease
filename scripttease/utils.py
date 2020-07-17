# Imports

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name

BashLexer = get_lexer_by_name("bash")
JSONLexer = get_lexer_by_name("json")
PythonLexer = get_lexer_by_name("python")
TerminalFormatter = get_formatter_by_name("terminal", linenos=True)

# Exports

__all__ = (
    "any_list_item",
    "filter_commands",
    "filter_objects",
    "highlight_code",
    "split_csv",
)

# Functions


def any_list_item(a, b):
    """Determine whether any item in ``a`` also exists in ``b``.

    :param a: The first list to be compared.
    :type a: list

    :param b: The second list to be compared.
    :type b: list

    :rtype: bool

    """
    for i in a:
        for j in b:
            if i == j:
                return True

    return False


def filter_commands(commands, values, attribute="tags"):
    """Filter commands for a given set of values.

    :param commands: The commands to be filtered.
    :type commands: list[BaseType[Command]]

    :param values: The values to be compared.
    :type values: list

    :param attribute: The name of the command attribute to check. This attribute must be a list or tuple of values of
                      the same type given in ``values``.
    :type attribute: str

    :rtype: bool

    .. code-block:: python

        commands = [
            AddUser("bob"),
            Apt("apache2", tags=["apache", "www"]),
            Reload("postgresql", tags=["database", "pgsql"]),
            Touch("/var/www/index.html", tags=["www"]),
        ]

        values = ["apache", "www"]

        # Outputs the Apt and Touch commands above.
        filtered_commands = filter_commands(command, values)
        print(filtered_commands)

    """
    filtered = list()
    for command in commands:
        try:
            list_b = getattr(command, attribute)
        except AttributeError:
            continue

        if not any_list_item(values, list_b):
            continue

        filtered.append(command)

    return filtered


def filter_objects(objects, environments=None, scope=None, tags=None):
    """Filter the given objects by the given keys.

    :param objects: The objects to be filtered.
    :type objects: list

    :param environments: The environments to be included.
    :type environments: list[str]

    :param scope: The scope by which to filter; deploy, provision, tenant.
    :type scope: str

    :param tags: The tags to be included.
    :type tags: list[str]

    :rtype: list
    :returns: Returns the objects that match the given keys.

    """
    filtered = list()

    # print("object, object environments, environments, any_list_item")

    for o in objects:

        # print(o, o.environments, environments, any_list_item(environments, o.environments))

        # Apply environment filter.
        if environments is not None:
            if hasattr(o, "environment"):
                if o.environment is not None and o.environment not in environments:
                    continue
            elif hasattr(o, "environments"):
                if type(o.environments) in (list, tuple) and not any_list_item(environments, o.environments):
                    continue
            else:
                pass

        # # Apply scope filter.
        # if scope is not None:
        #     if o.scope not in [None, SCOPE_ALL, scope]:
        #         continue

        # Apply tag filter.
        if tags is not None:
            if not any_list_item(tags, o.tags):
                continue

        # The object has passed the tests above.
        filtered.append(o)

    return filtered


def highlight_code(string, lexer=None):
    """Highlight (colorize) the given string as Python code.

    :param string: The string to be highlighted.
    :type string: str

    :rtype: str

    """
    if lexer is None:
        lexer = BashLexer

    return highlight(string, lexer, TerminalFormatter)


