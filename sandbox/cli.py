#! /usr/bin/env python

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from commonkit import highlight_code, smart_cast
from commonkit.logging import LoggingHelper
from commonkit.shell import EXIT
import sys

sys.path.insert(0, "../")

from scripttease.constants import LOGGER_NAME
from scripttease.lib.contexts import load_variables, Context
from scripttease.lib.loaders.ini import INILoader
from scripttease.lib.loaders.yaml import YMLLoader
from scripttease.version import DATE as VERSION_DATE, VERSION

DEBUG = 10

logging = LoggingHelper(colorize=True, name=LOGGER_NAME)
log = logging.setup()


def execute():
    """Process script configurations."""

    __author__ = "Shawn Davis <shawn@develmaycare.com>"
    __date__ = VERSION_DATE
    __help__ = """NOTES

This command is used to parse configuration files and output the commands.

"""
    __version__ = VERSION + "+new"

    # Main argument parser from which sub-commands are created.
    parser = ArgumentParser(description=__doc__, epilog=__help__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        "path",
        default="steps.ini",
        nargs="?",
        help="The path to the configuration file."
    )

    parser.add_argument(
        "-c",
        "--color",
        action="store_true",
        dest="color_enabled",
        help="Enable code highlighting for terminal output."
    )

    parser.add_argument(
        "-C=",
        "--context=",
        action="append",
        dest="variables",
        help="Context variables for use in pre-parsing the config and templates. In the form of: name:value"
    )

    parser.add_argument(
        "-d",
        "--docs",
        action="store_true",
        dest="docs_enabled",
        help="Output documentation instead of code."
    )

    parser.add_argument(
        "-D",
        "--debug",
        action="store_true",
        dest="debug_enabled",
        help="Enable debug output."
    )

    parser.add_argument(
        "-f=",
        "--filter=",
        action="append",
        dest="filters",
        help="Filter the commands in the form of: attribute:value"
    )

    parser.add_argument(
        "-o=",
        "--option=",
        action="append",
        dest="options",
        help="Common command options in the form of: name:value"
    )

    parser.add_argument(
        "-P=",
        "--profile=",
        choices=["centos", "ubuntu"],
        default="ubuntu",
        dest="profile",
        help="The OS profile to use."
    )

    parser.add_argument(
        "-T=",
        "--template-path=",
        action="append",
        dest="template_locations",
        help="The location of template files that may be used with the template command."
    )

    parser.add_argument(
        "-w=",
        "--write=",
        dest="output_file",
        help="Write the output to disk."
    )

    parser.add_argument(
        "-V=",
        "--variables-file=",
        dest="variables_file",
        help="Load variables from a file."
    )

    # Access to the version number requires special consideration, especially
    # when using sub parsers. The Python 3.3 behavior is different. See this
    # answer: http://stackoverflow.com/questions/8521612/argparse-optional-subparser-for-version
    parser.add_argument(
        "-v",
        action="version",
        help="Show version number and exit.",
        version=__version__
    )

    parser.add_argument(
        "--version",
        action="version",
        help="Show verbose version information and exit.",
        version="%(prog)s" + " %s %s by %s" % (__version__, __date__, __author__)
    )

    # Parse arguments.
    args = parser.parse_args()

    if args.debug_enabled:
        log.setLevel(DEBUG)

    log.debug("Namespace: %s" % args)

    # Create the global context.
    context = Context()

    if args.variables_file:
        variables = load_variables(args.variables_file)
        for v in variables:
            context.variables[v.name] = v

    if args.variables:
        for token in args.variables:
            try:
                key, value = token.split(":")
                context.add(key, smart_cast(value))
            except ValueError:
                context.add(token, True)

    # Capture filters.
    if args.filters:
        filters = dict()
        for token in args.filters:
            key, value = token.split(":")
            if key not in filters:
                filters[key] = list()

            filters[key].append(value)

    # Handle options.
    options = dict()
    if args.options:
        for token in args.options:
            try:
                key, value = token.split(":")
                options[key] = smart_cast(value)
            except ValueError:
                options[token] = True

    # Load the commands.
    if args.path.endswith(".ini"):
        loader = INILoader(
            args.path,
            context=context,
            locations=args.template_locations,
            profile=args.profile,
            **options
        )
    elif args.path.endswith(".yml"):
        loader = YMLLoader(
            args.path,
            context=context,
            locations=args.template_locations,
            profile=args.profile,
            **options
        )
    else:
        log.error("Unsupported file format: %s" % args.path)
        exit(EXIT.ERROR)

    # noinspection PyUnboundLocalVariable
    if not loader.load():
        exit(EXIT.ERROR)

    # Generate output.
    if args.docs_enabled:
        pass
    else:
        commands = list()
        for snippet in loader.get_snippets():
            # Skip explanations and screenshots. They don't produce usable statements.
            if snippet.name in ("explain", "screenshot"):
                continue

            statement = snippet.get_statement()
            if statement is not None:
                commands.append(statement)
                commands.append("")

        if args.color_enabled:
            print(highlight_code("\n".join(commands), language="bash"))
        else:
            print("\n".join(commands))

    exit(EXIT.OK)


if __name__ == '__main__':
    execute()


