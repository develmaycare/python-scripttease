# Django

Summary: Work with Django management commands.

## Common Options for Django Commands

You will generally want to include `cd` to change to the project directory and `prefix` to load the virtual environment.

```yaml
- collect static files:
  django: static
  cd: /path/to/project/source
  prefix: source ../python/bin/activate
```

## Automatic Conversion of Django Command Switches

Options provided in the command configuration file are automatically converted to command line switches.

```yaml
- run database migrations:
  django: migrate
  settings: tenants.example_com.settings

- dump some data:
  django: dumpdata
  indent: 4
  natural_foreign: yes
  natural_primary: yes
```

## Available Commands

### check

```ini
[run django checks]
django: check
```

```yaml
- run django checks:
  django: check
```

### dumpdata

Dump fixture data.

- app: Required. The name of the app.
- model: Optional. A model name within the app.
- path: The path to the JSON file. When a model is provided, this defaults to `fixtures/app/model.json`. Otherwise, it is `fixtures/app/initial.json`.

```ini
[dump project data]
django: dumpdata
app: projects

[dump project categories]
django: dumpdata
app: projects
model: Category
path: local/projects/fixtures/default-categories.json
```

### loaddata

Load fixture data.

- path: The path to the JSON file. When a model is provided, this defaults to `fixtures/app/model.json`. Otherwise, it is `fixtures/app/initial.json`.

### migrate

Run database migrations.

```ini
[run database migrations]
django: migrate
```

```yaml
- run database migrations:
  django: migrate
```

### static

Collect static files.

```ini
[collect static files]
django: static
```

```yaml
- collect static files:
  django: static
```

## Custom or Ad Hoc Commands

It is possible to work with any Django management command provided the parameters may be specified as a switch. 

```ini
[run any django command]
django: command_name
first_option_name: asdf
second_option_name: 1234
third_option_name: yes
```

```yaml
- run any django command:
  django: command_name
  first_option_name: asdf
  second_option_name: 1234
  third_option_name: yes
```
