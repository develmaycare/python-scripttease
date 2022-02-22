# Command File

A command file contains the metadata about the commands to be generated. INI and YAML formats are supported.

In an INI file, each section is a command. With YAML, each top-level list item is a command. 

## The Comment/Description

With INI files, the section name is the command comment.

```ini
[this becomes the command comment]
; ...
```

With YAML, each command is a list item and the item name becomes the command comment:

```yaml
- this becomes the command comment:
  # ...
```

## First Option and Arguments

The first variable in the section is the command name. It's value contains the required arguments.

```ini
[restart the postfix service]
restart: postfix
```

```yaml
- restart the postfix service:
  restart: postfix
```

## Formatting Notes

With both INI and YAML files, the formatting rules are:

- The first part of each command is the INI section or YAML item and is used as the comment.
- The command name *must* be the *first* option in the section.
- The arguments for the command appear as the value of the first option in the section. Arguments are separated by a
  space.
- Arguments that should be treated as a single value should be enclosed in double quotes.
- `yes` and `no` are interpreted as boolean values. `maybe` is interpreted as `None`.
- List values, where required, are separated by commas when appearing in INI files, but are a `[standard, list, of, values]` in a YAML file.

## Additional Attributes

Additional variables in the section are generally optional parameters that inform or control how the command should be executed and are sometimes used to add switches to the statement.

!!! warning

    This is not always the case, so consult the documentation for the command in question, because some parameters that appear after the first line are actually required.

## Common Attributes

A number of common options are recognized. Some of these have no bearing on statement generation but may be used for filtering. Others may be optionally included, and a few may only be used programmatically.

### cd

The `cd` option sets the directory (path) from which the statement should be executed. It is included by default when the statement is generated, but may be suppressed using `cd=False`.

```ini
[create a python virtual environment]
virtualenv: python
cd: /path/to/project
```

### comment

The comment comes from the section name (INI) or list name (YAML). It is included by default when the statement is generated, by may be suppressed using `include_comment=False`.

```ini
[this becomes the comment]
; ...
```

```yaml
- this becomes the comment:
  # ...
```

### env

The `env` option indicates the target environment (or environments) in which the statement should run. This is not used in command generation, but may be used for filtering.

```yaml
- set up the database:
  pgsql.create: example_com
  env: [staging, live]
```

This option may be given as `environments`, `environs`, `envs`, or simply `env`. It may be a list or CSV string.

### prefix

The `prefix` option is used to define a statement to be executed before the main statement is executed.

```ini
[migrate the database]
django: migrate
cd: /path/to/project/source
prefix: source ../python/bin/activate
```

### register

`register` defines the name of a variable to which the result of the statement should be saved. It is included by default when the statement is generated, but may be suppressed using `include_register=False`.

```yaml
- check apache configuration:
  apache: test
  register: apache_ok
```

### shell

The `shell` defines the shell to be used for command execution. It is not used for statement generation, but may be used programmatically -- for example, with Python's subprocess module. Some commands (such as Django management commands) need a shell to be explicitly defined.

```ini
[run django checks]
django: check
cd: /path/to/project/source
prefix: source ../python/bin/activate
shell: /bin/bash
```

!!! note

    As this option is intended for programmatic use, it would be better to define a default shell for all command execution and use this option only when the default should be overridden. 

### stop

A `yes` indicates processing should stop if the statement fails to execute with success. It is included by default when the statement is generated, but may be suppressed. Additionally, when [register](#register) is defined, this option will use the result of the command to determine success. This option is also useful for programmatic execution.

```yaml
- check apache configuration:
  apache: test
  register: apache_ok
  stop: yes
```

!!! warning

    Some commands do not provide an zero or non-zero exit code on success or failure. You should verify that the `stop` will actually be used.

### sudo

The `sudo` option may be defined as `yes` or a username. This will cause the statement to be generated with sudo.

```ini
[install apache]
install: apache2
sudo: yes
```

!!! note

    When present, sudo is always generated as part of the statement. For programmatic use, it may be better to control how and when sudo is applied using some other mechanism. If sudo should be used for all statements, it can be passed as a global option.

### tags

`tags` is a comma separated list (INI) or list (YAML) of tag names. These may be used for filtering.

```yaml
- install apache:
  install: apache2
  tags: [apache, web]
  
- enable wsgi:
  apache.enable: mod_wsgi
  tags: [apache, web]
  
- restart apache:
  apache.restart:
  tags: [apache, web]

- run django checks:
  django: check
  tags: [django, python]

- apply database migrations:
  django: migrate
  tags: [django, python]
```

## Ad Hoc Options

Options that are not recognized as common or as part of those specific to a command are still processed by the loader. This makes it possible to define your own options based on the needs of a given implementation.

For example, suppose you are implementing a deployment system where some commands should run locally, but most should run on the remote server.

```ini
[run tests to validate the system]
run: make tests
local: yes
stop: yes

[install apache]
install: apache2
remote: yes

; and so on ...
```

This will be of no use as a generated script since the generator does not know about `local` and `remote`, but these could be used programmatically to control whether Python subprocess or an SSH client is invoked.
