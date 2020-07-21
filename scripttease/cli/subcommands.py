# Imports

from superpython.shell import EXIT
from superpython.utils import highlight_code
from ..parsers import load_commands, load_config

# Functions


def output_commands(path, color_enabled=False, context=None, filters=None, locations=None, options=None):
    commands = load_commands(
        path,
        context=context,
        filters=filters,
        locations=locations,
        options=options
    )
    if commands is None:
        return EXIT.ERROR

    output = list()
    for command in commands:
        statement = command.get_statement(cd=True)
        if statement is None:
            continue

        output.append(statement)
        output.append("")

    if color_enabled:
        print(highlight_code("\n".join(output), language="bash"))
    else:
        print("\n".join(output))

    return EXIT.OK


def output_docs(path, context=None, filters=None, locations=None, options=None):
    commands = load_commands(
        path,
        context=context,
        filters=filters,
        locations=locations,
        options=options
    )
    if commands is None:
        return EXIT.ERROR

    count = 1
    output = list()
    for command in commands:
        output.append("%s. %s" % (count, command.comment))
        count += 1

    print("\n".join(output))

    return EXIT.OK


def output_script(path, color_enabled=False, context=None, filters=None, locations=None, options=None):
    config = load_config(
        path,
        context=context,
        locations=locations,
        options=options
    )
    if config is None:
        return EXIT.ERROR

    script = config.as_script()
    if color_enabled:
        print(highlight_code(script.to_string(), language="bash"))
    else:
        print(script)

    return EXIT.OK
