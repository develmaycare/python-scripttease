# Python Script Tease

## Overview

Script Tease is a library and command line tool for generating Bash commands programmatically and (especially) using configuration files.

The primary focus (and limit) is to convert plain text instructions (in INI or YAML format) into valid command line statements for a given platform. It does *not* provide support for executing those statements.

## Concepts

### Command Generation

Script Tease may be used in two (2) ways:

1. Using the library to programmatically define commands and export them as command line statements. 
2. Using the `tease` command to generate commands from a configuration file. See [command file configuration](config/command-file.md).

This documentation focuses on the second method, but the developer docs may be used in your own implementation.

### Self-Documenting

The format of INI and YAML files is self-documenting. The command comment is this section (INI) or start of a list item (YAML). This ensures that all commands have a basic description of their purpose or intent.

### Snippets

An *snippet* is simply a tokenized command that may be customized based on the instructions found in a command file. Related snippets are collected into groups and then merged into a larger set that define the capabilities of a specific operating system.

!!! note
    At present, the only fully defined operating systems are for Cent OS and Ubuntu.

Snippets are defined in Python dictionaries. These include a "canonical" command name as the key and either a string or list which define the command. In both cases, the contents are parsed as Jinja templates. There are various approaches to evaluating  a snippet.

First: The snippet is a simple mapping of command name and command snippet. This is easy. Find the command name in the dictionary, and we have the snippet to be used. For example the `append` command in the `posix` dictionary.

Second: The snippet is a mapping of command name and a list of snippets to be combined. Find the command name in the dictionary, and iterate through the snippets. For example, many of the commands in the `posix` dictionary takes this form. Command identification is the same as the first condition.

Third: The command is a mapping to informal sub-commands. Examples include `apache` and `system` in the `ubuntu` dictionary. There are a couple of ways to handle this in the config file:

- Use the outer command as the command with the inner command as the first (and perhaps only) argument. For example `apache: reload` or `system: upgrade`.
- Use a "dotted path" to find the command. For example: `apache.reload: (implicity True)` or `system.upgrade: (implicitly True)`. Or `apache.enable_site: example.com`.

The first approach complicates things when detecting actual sub-commands (below). Script Tease supports both of these approaches.

Fourth: The command also expects a sub-command. In some cases, the sub-command may be implicit, like `pip install`. In other cases, a number of sub-commands may be pre-defined, but ad hoc sub-commands should also be supported as with Django commands.

Fifth: Builds upon the third and fourth conditions where the commands have lots of options, some of which may be defined at runtime. Postgres and MySQL may use be presented as informal sub-commands, but there are lots of options and challenges in building the final command. Django management commands have a number of standard options, specific options, and must also support ad hoc commands.

## Terms and Definitions

command
:   When used in Script Tease documentation, this is a command instance which contains the properties and parameters for a command line statement.

statement
:   A specific statement (string) to be executed. A *statement* is contained within a *command*.

## License

Python Script Tease is released under the BSD 3 clause license.
