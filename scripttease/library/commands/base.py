# Classes


class Command(object):

    def __init__(self, statement, comment=None, condition=None, cd=None, environments=None, function=None, prefix=None,
                 register=None, shell=None, stop=False, sudo=None, tags=None, **kwargs):
        self.comment = comment
        self.condition = condition
        self.cd = cd
        self.environments = environments or list()
        self.function = function
        self.prefix = prefix
        self.register = register
        self.shell = shell
        self.statement = statement
        self.stop = stop
        self.tags = tags or list()

        if isinstance(sudo, Sudo):
            self.sudo = sudo
        elif type(sudo) is str:
            self.sudo = Sudo(enabled=True, user=sudo)
        elif sudo is True:
            self.sudo = Sudo(enabled=True)
        else:
            self.sudo = Sudo()

        self._attributes = kwargs

    def __getattr__(self, item):
        return self._attributes.get(item)

    def __repr__(self):
        if self.comment is not None:
            return "<%s %s>" % (self.__class__.__name__, self.comment)

        return "<%s>" % self.__class__.__name__

    def get_statement(self, cd=False):
        """Get the full statement.

        :param cd: Include the directory change, if given.
        :type cd: bool

        :rtype: str

        """
        a = list()

        if cd and self.cd is not None:
            a.append("( cd %s &&" % self.cd)

        if self.prefix is not None:
            a.append("%s &&" % self.prefix)

        if self.sudo:
            statement = "sudo -u %s %s" % (self.sudo.user, self._get_statement())
        else:
            statement = self._get_statement()

        a.append("%s" % statement)

        if cd and self.cd is not None:
            a.append(")")

        b = list()
        if self.comment is not None:
            b.append("# %s" % self.comment)

        if self.condition is not None:
            b.append("if [[ %s ]]; then %s; fi;" % (self.condition, " ".join(a)))
        else:
            b.append(" ".join(a))

        if self.register is not None:
            b.append("%s=$?;" % self.register)

            if self.stop:
                b.append("if [[ $%s -gt 0 ]]; exit 1; fi;" % self.register)
        elif self.stop:
            b.append("if [[ $? -gt 0 ]]; exit 1; fi;")
        else:
            pass

        return "\n".join(b)

    def _get_statement(self):
        """By default, get the statement passed upon command initialization.

        :rtype: str

        """
        return self.statement


class ItemizedCommand(object):

    def __init__(self, command_class, items, *args, **kwargs):
        """Initialize the command.

        :param command_class: The command class to be used.
        :type command_class: class

        :param items: The command arguments.
        :type items: list[str]

        :param args: The itemized arguments. ``$item`` should be included.

        :param kwargs: Keyword arguments are passed to the command class upon instantiation.

        """
        self.args = args
        self.command_class = command_class
        self.items = items
        self.kwargs = kwargs

    def __getattr__(self, item):
        return self.kwargs.get(item)

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.command_class.__name__)

    def get_commands(self):
        """Get the commands to be executed.

        :rtype: list[BaseType(Command)]

        """
        kwargs = self.kwargs.copy()

        a = list()
        for item in self.items:
            args = list()
            for arg in self.args:
                args.append(arg.replace("$item", item))

            command = self.command_class(*args, **kwargs)
            a.append(command)

        return a

    def get_statement(self, cd=False):
        """Override to get multiple commands."""
        kwargs = self.kwargs.copy()
        comment = kwargs.pop("comment", "execute multiple commands")

        a = list()
        # a.append("# %s" % comment)

        commands = self.get_commands()
        for c in commands:
            a.append(c.get_statement(cd=cd))
            a.append("")

        # for item in self.items:
        #     args = list()
        #     for arg in self.args:
        #         args.append(arg.replace("$item", item))
        #
        #     command = self.command_class(*args, **kwargs)
        #     a.append(command.preview(cwd=cwd))
        #     a.append("")

        return "\n".join(a)


class Sudo(object):
    """Helper class for defining sudo options."""

    def __init__(self, enabled=False, user="root"):
        """Initialize the helper.

        :param enabled: Indicates sudo is enabled.
        :type enabled: bool

        :param user: The user to be invoked.
        :type user: str

        """
        self.enabled = enabled
        self.user = user

    def __bool__(self):
        return self.enabled
