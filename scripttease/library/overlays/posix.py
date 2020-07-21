# Imports

import os
from superpython.utils import indent
from ..commands import Command

# Exports

__all__ = (
    "POSIX_MAPPINGS",
    "archive",
    "certbot",
    "extract",
    "file_append",
    "file_copy",
    "file_write",
    "mkdir",
    "move",
    "perms",
    "remove",
    "rsync",
    "run",
    "scopy",
    "sed",
    "symlink",
    "touch",
    "Function",
)

# Functions


def archive(from_path, absolute=False, exclude=None, file_name="archive.tgz", strip=None, to_path=".", view=False,
            **kwargs):
    """Create a file archive.

    :param from_path: The path that should be archived.
    :type from_path: str

    :param absolute: By default, the leading slash is stripped from each path. Set to ``True`` to preserve the
                     absolute path.
    :type absolute: bool

    :param bzip2: Compress using bzip2.
    :type bzip2: bool

    :param exclude: A pattern to be excluded from the archive.
    :type exclude: str

    :param format: The command to use for the operation.
    :type format: str

    :param gzip: Compress using gzip.
    :type gzip: bool

    :param strip: Remove the specified number of leading elements from the path. Paths with fewer elements will be
                  silently skipped.
    :type strip: int

    :param to_path: Where the archive should be created. This should *not* include the file name.
    :type to_path: str

    :param view: View the output of the command as it happens.
    :type view: bool

    """
    tokens = ["tar"]
    switches = ["-cz"]

    if absolute:
        switches.append("P")

    if view:
        switches.append("v")

    tokens.append("".join(switches))

    if exclude:
        tokens.append("--exclude %s" % exclude)

    if strip:
        tokens.append("--strip-components %s" % strip)

    to_path = os.path.join(to_path, file_name)
    tokens.append('-f %s %s' % (to_path, from_path))

    name = " ".join(tokens)

    return Command(name, **kwargs)


def certbot(domain_name, email=None, webroot=None, **kwargs):
    """Get new SSL certificate from Let's Encrypt.

    :param domain_name: The domain name for which the SSL certificate is requested.
    :type domain_name: str

    :param email: The email address of the requester sent to the certificate authority. Required.
    :type email: str

    :param webroot: The directory where the challenge file will be created.
    :type webroot: str

    """
    _email = email or os.environ.get("SCRIPTTEASE_CERTBOT_EMAIL", None)
    _webroot = webroot or os.path.join("/var", "www", "domains", domain_name.replace(".", "_"), "www")

    if not _email:
        raise ValueError("Email is required for certbot command.")

    template = "certbot certonly --agree-tos --email %(email)s -n --webroot -w %(webroot)s -d %(domain_name)s"
    name = template % {
        'domain_name': domain_name,
        'email': _email,
        'webroot': _webroot,
    }

    return Command(name, **kwargs)


def extract(from_path, absolute=False, exclude=None, strip=None, to_path=None, view=False, **kwargs):
    """Extract a file archive.

    :param from_path: The path to the archive file.
    :type from_path: str

    :param absolute: By default, the leading slash is stripped from each path. Set to ``True`` to preserve the
                     absolute path.
    :type absolute: bool

    :param exclude: A pattern to be excluded from the archive.
    :type exclude: str

    :param strip: Remove the specified number of leading elements from the path. Paths with fewer elements will be
                  silently skipped.
    :type strip: int

    :param to_path: Where the archive should be extracted.
    :type to_path: str

    :param view: View the output of the command as it happens.
    :type view: bool

    """
    _to_path = to_path or "./"

    tokens = ["tar"]
    switches = ["-xz"]

    if absolute:
        switches.append("P")

    if view:
        switches.append("v")

    tokens.append("".join(switches))

    if exclude:
        tokens.append("--exclude %s" % exclude)

    if strip:
        tokens.append("--strip-components %s" % strip)

    tokens.append('-f %s %s' % (from_path, _to_path))

    name = " ".join(tokens)

    return Command(name, **kwargs)


def file_append(path, content=None, **kwargs):
    """Append content to a file.

    :param path: The path to the file.
    :type path: str

    :param content: The content to be appended.
    :type content: str

    """
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


def file_write(path, content=None, **kwargs):
    """Initialize the command.

    :param path: The file to be written.
    :type path: str

    :param content: The content to be written. Note: If omitted, this command is equivalent to :py:class:`Touch`.
    :type content: str

    """
    _content = content or ""

    kwargs.setdefault("comment", "write to %s" % path)

    a = list()

    if len(_content.split("\n")) > 1:
        a.append("cat > %s << EOF" % path)
        a.append(_content)
        a.append("EOF")
    else:
        a.append('echo "%s" > %s' % (_content, path))

    return Command(" ".join(a), **kwargs)


def mkdir(path, mode=None, recursive=True, **kwargs):
    """Initialize the command.

    :param path: The path to be created.
    :type path: str

    :param mode: The access permissions of the new directory.
    :type mode: int | str

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
    :type mode: int | str

    :param owner: The name of the user to be applied.
    :type owner: str

    :param recursive: Create all directories along the path.
    :type recursive: bool

    """
    commands = list()

    kwargs['comment'] = "set permissions on %s" % path

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
        a.append(c.get_statement(suppress_comment=True))

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


def rsync(source, target, delete=False, exclude=None, host=None, key_file=None, links=True, port=22,
          recursive=True, user=None, **kwargs):
    """Initialize the command.

    :param source: The source directory.
    :type source: str

    :param target: The target directory.
    :type target: str

    :param delete: Indicates target files that exist in source but not in target should be removed.
    :type delete: bool

    :param exclude: The path to an exclude file.
    :type exclude: str

    :param host: The host name or IP address. This causes the command to run over SSH and may require a
                 ``key_file``, ``port``, and ``user``.
    :type host: str

    :param key_file: The path to the private SSH key to use for remove connections. User expansion is
                     automatically applied.
    :type key_file: str

    :param links: Include symlinks in the sync.
    :type links: bool

    :param port: The SSH port to use for remote connections.
    :type port: int

    :param recursive: Indicates source contents should be recursively synchronized.
    :type recursive: bool

    :param user: The user name to use for remote connections.

    """
    # :param guess: When ``True``, the ``host``, ``key_file``, and ``user`` will be guessed based on the base name of
    #               the source path.
    # :type guess: bool
    # if guess:
    #     host = host or os.path.basename(source).replace("_", ".")
    #     key_file = key_file or os.path.expanduser(os.path.join("~/.ssh", os.path.basename(source)))
    #     user = user or os.path.basename(source)
    # else:
    #     host = host
    #     key_file = key_file
    #     user = user

    kwargs.setdefault("comment", "copy %s to remote %s" % (source, target))

    # rsync -e "ssh -i $(SSH_KEY) -p $(SSH_PORT)" -P -rvzc --delete
    # $(OUTPUTH_PATH) $(SSH_USER)@$(SSH_HOST):$(UPLOAD_PATH) --cvs-exclude;

    tokens = list()
    tokens.append('rsync')
    tokens.append("--cvs-exclude")
    tokens.append("--checksum")
    tokens.append("--compress")

    if links:
        tokens.append("--copy-links")

    if delete:
        tokens.append("--delete")

    if exclude is not None:
        tokens.append("--exclude-from=%s" % exclude)

    # --partial and --progress
    tokens.append("-P")

    if recursive:
        tokens.append("--recursive")

    tokens.append(source)

    conditions = [
        host is not None,
        key_file is not None,
        user is not None,
    ]
    if all(conditions):
        tokens.append('-e "ssh -i %s -p %s"' % (key_file, port))
        tokens.append("%s@%s:%s" % (user, host, target))
    else:
        tokens.append(target)

    statement = " ".join(tokens)

    return Command(statement, **kwargs)


def run(statement, **kwargs):
    """Run any statement."""
    kwargs.setdefault("comment", "run statement")
    return Command(statement, **kwargs)


def scopy(from_path, to_path, host=None, key_file=None, port=22, user=None, **kwargs):
        """Initialize the command.

        :param from_path: The source directory.
        :type from_path: str

        :param to_path: The target directory.
        :type to_path: str

        :param host: The host name or IP address. Required.
        :type host: str

        :param key_file: The path to the private SSH key to use for remove connections. User expansion is
                         automatically applied.
        :type key_file: str

        :param port: The SSH port to use for remote connections.
        :type port: int

        :param user: The user name to use for remote connections.

        """
        kwargs.setdefault("comment", "copy %s to remote %s" % (from_path, to_path))

        # TODO: What to do to force local versus remote commands?
        # kwargs['local'] = True

        kwargs['sudo'] = False

        statement = ["scp"]

        if key_file is not None:
            statement.append("-i %s" % key_file)

        statement.append("-P %s" % port)
        statement.append(from_path)

        if host is not None and user is not None:
            statement.append("%s@%s:%s" % (user, host, to_path))
        elif host is not None:
            statement.append("%s:%s" % (host, to_path))
        else:
            raise ValueError("Host is a required keyword argument.")

        return Command(" ".join(statement), **kwargs)


def sed(path, backup=".b", delimiter="/", find=None, replace=None, **kwargs):
    """Find and replace text in a file.

    :param path: The path to the file to be edited.
    :type path: str

    :param backup: The backup file extension to use.
    :type backup: str

    :param delimiter: The pattern delimiter.

    :param find: The old text. Required.
    :type find: str

    :param replace: The new text. Required.
    :type replace: str

    """

    kwargs.setdefault("comment", "find and replace in %s" % path)

    context = {
        'backup': backup,
        'delimiter': delimiter,
        'path': path,
        'pattern': find,
        'replace': replace,
    }

    template = "sed -i %(backup)s 's%(delimiter)s%(pattern)s%(delimiter)s%(replace)s%(delimiter)sg' %(path)s"

    statement = template % context

    return Command(statement, **kwargs)


def symlink(source, force=False, target=None, **kwargs):
    """Initialize the command.

    :param source: The source of the link.
    :type source: str

    :param force: Force the creation of the link.
    :type force: bool

    :param target: The name or path of the target. Defaults to the base name of the source path.
    :type target: str

    """
    _target = target or os.path.basename(source)

    kwargs.setdefault("comment", "link to %s" % source)

    statement = ["ln -s"]

    if force:
        statement.append("-f")

    statement.append(source)
    statement.append(_target)

    return Command(" ".join(statement), **kwargs)


def touch(path, **kwargs):
    """Initialize the command.

    :param path: The file or directory to touch.
    :type path: str

    """
    kwargs.setdefault("comment", "touch %s" % path)

    return Command("touch %s" % path, **kwargs)

# Classes


class Function(object):
    """A function that may be used to organize related commands to be called together."""

    def __init__(self, name, commands=None, comment=None):
        self.commands = commands or list()
        self.comment = comment
        self.name = name

    def to_string(self):
        a = list()

        if self.comment is not None:
            a.append("# %s" % self.comment)

        a.append("function %s()" % self.name)
        a.append("{")
        for command in self.commands:
            a.append(indent(command.get_statement(cd=True)))
            a.append("")

        a.append("}")

        return "\n".join(a)

# Mappings


POSIX_MAPPINGS = {
    'append': file_append,
    'archive': archive,
    'certbot': certbot,
    'copy': file_copy,
    'extract': extract,
    'func': Function,
    'function': Function,
    'mkdir': mkdir,
    'move': move,
    'perms': perms,
    'remove': remove,
    'rsync': rsync,
    'run': run,
    'scopy': scopy,
    'sed': sed,
    'ssl': certbot,
    'symlink': symlink,
    'touch': touch,
    'write': file_write,
}
