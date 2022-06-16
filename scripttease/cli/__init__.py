# Imports

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from commonkit.logging import LoggingHelper
from ..variables import LOGGER_NAME, PATH_TO_SCRIPT_TEASE
from ..version import DATE as VERSION_DATE, VERSION
from . import initialize
from . import subcommands

# New:
from commonkit import highlight_code, indent, smart_cast, write_file
from commonkit.shell import EXIT
from markdown import markdown
import os
from scripttease.lib.contexts import Context
from scripttease.lib.factories import command_factory
from scripttease.lib.loaders import load_variables, INILoader, YMLLoader

DEBUG = 10

logging = LoggingHelper(colorize=True, name=LOGGER_NAME)
log = logging.setup()

# Commands


def execute():
    """Process script configurations."""

    __author__ = "Shawn Davis <shawn@develmaycare.com>"
    __date__ = VERSION_DATE
    __help__ = """NOTES

    This command is used to parse configuration files and output the commands.

        """
    __version__ = VERSION

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
        "-d=",
        "--docs=",
        choices=["html", "markdown", "plain", "rst"],
        # default="markdown",
        dest="docs",
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
        "-i=",
        "--inventory=",
        dest="inventory",
        help="Copy an inventory item to a local directory."
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

    # Handle global command options.
    options = dict()
    if args.options:
        for token in args.options:
            try:
                key, value = token.split(":")
                options[key] = smart_cast(value)
            except ValueError:
                options[token] = True

    # The path may have been given as a file name (steps.ini), path, or an inventory name.
    input_locations = [
        args.path,
        os.path.join(PATH_TO_SCRIPT_TEASE, "data", "inventory", args.path, "steps.ini"),
        os.path.join(PATH_TO_SCRIPT_TEASE, "data", "inventory", args.path, "steps.yml"),
    ]
    path = None
    for location in input_locations:
        if os.path.exists(location):
            path = location
            break

    if path is None:
        log.warning("Path does not exist: %s" % args.path)
        exit(EXIT.INPUT)

    # Load the commands.
    if path.endswith(".ini"):
        loader = INILoader(
            path,
            context=context,
            locations=args.template_locations,
            profile=args.profile,
            **options
        )
    elif path.endswith(".yml"):
        loader = YMLLoader(
            path,
            context=context,
            locations=args.template_locations,
            profile=args.profile,
            **options
        )
    else:
        log.error("Unsupported file format: %s" % path)
        exit(EXIT.ERROR)

    # noinspection PyUnboundLocalVariable
    if not loader.load():
        log.error("Failed to load the input file: %s" % path)
        exit(EXIT.ERROR)

    # Generate output.
    if args.docs:
        output = list()
        for command in loader.commands:

            # Will this every happen?
            # if command is None:
            #     continue

            if command.name == "explain":
                if command.header:
                    if args.docs == "plain":
                        output.append("***** %s *****" % command.name.title())
                    elif args.docs == "rst":
                        output.append(command.name.title())
                        output.append("=" * len(command.name))
                    else:
                        output.append("## %s" % command.name.title())

                    output.append("")

                output.append(command.content)
                output.append("")
            elif command.name == "screenshot":
                if args.docs == "html":
                    b = list()
                    b.append('<img src="%s"' % command.args[0])
                    b.append('alt="%s"' % command.caption or command.comment)

                    if command.classes:
                        b.append('class="%s"' % command.classes)

                    if command.height:
                        b.append('height="%s"' % command.height)

                    if command.width:
                        b.append('width="%s"' % command)

                    output.append(" ".join(b) + ">")
                    output.append("")
                elif args.docs == "plain":
                    output.append(command.args[0])
                    output.append("")
                elif args.docs == "rst":
                    output.append(".. figure:: %s" % command.args[0])

                    if command.caption:
                        output.append(indent(":alt: %s" % command.caption or command.comment))

                    if command.height:
                        output.append(indent(":height: %s" % command.height))

                    if command.width:
                        output.append(indent(":width: %s" % command.width))

                    output.append("")
                else:
                    output.append("![%s](%s)" % (command.caption or command.comment, command.args[0]))
                    output.append("")
            elif command.name == "template":
                if args.docs == "plain":
                    output.append("+++")
                    output.append(command.get_content())
                    output.append("+++")
                elif args.docs == "rst":
                    output.append(".. code-block:: %s" % command.get_target_language())
                    output.append("")
                    output.append(indent(command.get_content()))
                    output.append("")
                else:
                    output.append("```%s" % command.get_target_language())
                    output.append(command.get_content())
                    output.append("```")
                    output.append("")
            else:
                statement = command.get_statement(include_comment=False, include_register=False, include_stop=False)
                if statement is not None:
                    line = command.comment.replace("#", "")
                    output.append("%s:" % line.capitalize())
                    output.append("")
                    if args.docs == "plain":
                        output.append("---")
                        output.append(statement)
                        output.append("---")
                        output.append("")
                    elif args.docs == "rst":
                        output.append(".. code-block:: bash")
                        output.append("")
                        output.append(indent(statement))
                        output.append("")
                    else:
                        output.append("```bash")
                        output.append(statement)
                        output.append("```")
                        output.append("")

        if args.docs == "html":
            _output = markdown("\n".join(output), extensions=['fenced_code'])
        else:
            _output = "\n".join(output)

        print(_output)

        if args.output_file:
            write_file(args.output_file, _output)
    else:
        commands = command_factory(loader)
        output = list()
        for command in commands:
            # print("COMMAND", command)
            # Explanations and screenshots don't produce usable statements but may be added as comments.
            if command.name in ("explain", "screenshot"):
                # commands.append("# %s" % command.content)
                # commands.append("")
                continue

            statement = command.get_statement(include_comment=False)
            if statement is not None:
                output.append(statement)
                output.append("")

        if args.color_enabled:
            print(highlight_code("\n".join(output), language="bash"))
        else:
            print("\n".join(output))

        if args.output_file:
            write_file(args.output_file, "\n".join(output))

    exit(EXIT.OK)


def main_command():
    """Process script configurations."""

    __author__ = "Shawn Davis <shawn@develmaycare.com>"
    __date__ = VERSION_DATE
    __help__ = """NOTES

This command is used to parse configuration files and output the commands.

    """
    __version__ = VERSION

    # Main argument parser from which sub-commands are created.
    parser = ArgumentParser(description=__doc__, epilog=__help__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        "path",
        default="commands.ini",
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

    # parser.add_argument(
    #     "-d=",
    #     "--docs=",
    #     choices=["html", "markdown", "plain", "rst"],
    #     dest="docs_enabled",
    #     help="Output documentation instead of code."
    # )

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
        "-O=",
        "--option=",
        action="append",
        dest="options",
        help="Common command options in the form of: name:value"
    )

    # parser.add_argument(
    #     "-O=",
    #     "--output=",
    #     # default=os.path.join("prototype", "output"),
    #     dest="output_path",
    #     help="Output to the given directory. Defaults to ./prototype/output/"
    # )

    parser.add_argument(
        "-s",
        "--script",
        action="store_true",
        dest="script_enabled",
        help="Output commands as a script."
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

    # Load context.
    context = dict()
    if args.variables:
        context = initialize.context_from_cli(args.variables)

    # Load additional context from file.
    if args.variables_file:
        variables = initialize.variables_from_file(args.variables_file)
        if variables:
            context.update(variables)

    # Handle filters.
    filters = None
    if args.filters:
        filters = initialize.filters_from_cli(args.filters)

    # Handle options.
    options = None
    if args.options:
        options = initialize.options_from_cli(args.options)

    # Process the request.
    if args.docs_enabled:
        exit_code = subcommands.output_docs(
            args.path,
            context=context,
            filters=filters,
            locations=args.template_locations,
            options=options
        )
    elif args.script_enabled:
        exit_code = subcommands.output_script(
            args.path,
            color_enabled=args.color_enabled,
            context=context,
            locations=args.template_locations,
            options=options
        )
    else:
        exit_code = subcommands.output_commands(
            args.path,
            color_enabled=args.color_enabled,
            context=context,
            filters=filters,
            locations=args.template_locations,
            options=options
        )

    exit(exit_code)
