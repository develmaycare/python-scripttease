from ..commands import Command


def file_append(path, content=None, **kwargs):
    """Append content to a file.

    :param path: The path to the file.
    :type path: str

    :param content: The content to be appended.
    :type content: str

    """
    print("HERE")
    kwargs.setdefault("comment", "append to %s" % path)

    statement = 'echo "%s" >> %s' % (content or "", path)

    return Command(statement, **kwargs)


def file_copy(from_path, to_path, overwrite=False, recursive=False, **kwargs):
    """Initialize the command.

    :param from_path: The file or directory to be copied.
    :type from_path: str

    :param to_path: The location to which the file or directory should be copied.
    :type to_path: str

    :param overwrite: Indicates files and directories should be overwritten if they exist.
    :type overwrite: bool

    :param recursive: Copy sub-directories.
    :type recursive: bool

    """
    kwargs.setdefault("comment", "copy %s to %s" % (from_path, to_path))

    a = list()
    a.append("cp")

    if not overwrite:
        a.append("-n")

    if recursive:
        a.append("-R")

    a.append(from_path)
    a.append(to_path)

    return Command(" ".join(a), **kwargs)


def mkdir(path, mode=None, recursive=True, **kwargs):
    """Initialize the command.

    :param path: The path to be created.
    :type path: str

    :param mode: The access permissions of the new directory.
    :type mode: str

    :param recursive: Create all directories along the path.
    :type recursive: bool

    """
    kwargs.setdefault("comment", "create directory %s" % path)

    statement = ["mkdir"]
    if mode is not None:
        statement.append("-m %s" % mode)

    if recursive:
        statement.append("-p")

    statement.append(path)

    return Command(" ".join(statement), **kwargs)


def move(from_path, to_path, **kwargs):
    kwargs.setdefault("comment", "move %s to %s" % (from_path, to_path))
    statement = "mv %s %s" % (from_path, to_path)

    return Command(statement, **kwargs)


def perms(path, group=None, mode=None, owner=None, recursive=False, **kwargs):
    """Initialize the command.

    :param path: The path to be changed.
    :type path: str

    :param group: The name of the group to be applied.
    :type group: str

    :param mode: The access permissions of the file or directory.
    :type mode: str

    :param owner: The name of the user to be applied.
    :type owner: str

    :param recursive: Create all directories along the path.
    :type recursive: bool

    """
    commands = list()

    if group is not None:
        statement = ["chgrp"]

        if recursive:
            statement.append("-R")

        statement.append(group)
        statement.append(path)

        commands.append(Command(" ".join(statement), **kwargs))

    if owner is not None:
        statement = ["chown"]

        if recursive:
            statement.append("-R")

        statement.append(owner)
        statement.append(path)

        commands.append(Command(" ".join(statement), **kwargs))

    if mode is not None:
        statement = ["chmod"]

        if recursive:
            statement.append("-R")

        statement.append(str(mode))
        statement.append(path)

        commands.append(Command(" ".join(statement), **kwargs))

    kwargs.setdefault("comment", "set permissions on %s" % path)

    a = list()
    for c in commands:
        a.append(c.get_statement())

    return Command("\n".join(a), **kwargs)


def remove(path, force=False, recursive=False, **kwargs):
    """Initialize the command.

    :param path: The path to be removed.
    :type path: str

    :param force: Force the removal.
    :type force: bool

    :param recursive: Remove all directories along the path.
    :type recursive: bool

    """
    kwargs.setdefault("comment", "remove %s" % path)

    statement = ["rm"]

    if force:
        statement.append("-f")

    if recursive:
        statement.append("-r")

    statement.append(path)

    return Command(" ".join(statement), **kwargs)
