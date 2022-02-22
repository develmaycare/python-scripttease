# Variables File

A variables file contains variable definitions that may be used as the context for parsing a [command file](command-file.md) *before* the actual commands are generated.

Unlike a command file, the INI format is the only supported format for a variables file.

## The Variable Name

The variable name is defined in the section:

```ini
[domain_name]
value: example.com
```

## The Variable Value

As seen in the example above, the value is defined by simply adding a variable parameter:

```ini
[domain_name]
value: example.com

[database_host]
value: db1.example.com
```

!!! note
    
    This is the minimum definition for all variables.

## Defining An Environment

You may define an environment for any given variable that may be used for filtering variables. This is done by adding the environment name to the variable name:

```ini
[database_host:development]
comment: Local host used in development.
value: localhost

[database_host:live]
value: db1.example.com
```

In this way, variables of the same name may be supported across different deployment environments.

## Adding Comments

As demonstrated in the example above, you may comment on a variable by adding a `comment:` attribute to the section.

## Defining Tags

Tags may be defined for any variable as a comma separated list. This is useful for filtering.

```ini
[database_host:development]
value: localhost
tags: database

[database_host:live]
value: db1.example.com
tags: database

[domain_name]
value: example.app
tags: application
```

## Other Attributes

Any other variable defined in the section is dynamically available.

```ini
[domain_name]
value: example.app
other: test
```

The value of `other` is `test`.
