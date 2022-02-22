# CentOS

## Available Commands

The `centos` profile incorporates commands from [Django](../commands/django.md), [messages](../commands/messages.md), [MySQL](../commands/mysql.md), [PHP](../commands/php.md), [POSIX](../commands/posix.md), [Postgres](../commands/pgsql.md), and [Python](../commands/python.md). 

### apache

Work with Apache.

- `apache.disable_module: module_name` (not supported)
- `apache.disable_site: site_name` (not supported)
- `apache.enable_module: module_name` (not supported)
- `apache.enable_site: site_name` (not supported)
- `apache.reload`
- `apache.restart`
- `apache.start`
- `apache.stop`
- `apache.test` 

### install

Install a system package.

```ini
[install apache]
install: apache2
```

### reload

Reload a service.

```ini
[reload postgres]
reload: postgresql
```

### restart

Restart a service:

```ini
[restart postgres]
restart: postgresql
```

### run

Run any shell command.

```ini
[run a useless listing command]
run: "ls -ls"
```

Note that commands with arguments will need to be in quotes.

### start

Start a service:

```ini
[start postgres]
start: postgresql
```

### stop

Stop a service:

```ini
[stop postgres]
stop: postgresql
```

### system

With with the system.

- `system.reboot`
- `system.update`
- `system.upgrade`

### uninstall

Uninstall a package.

```ini
[remove libxyz development package]
uninstall: libxyz-dev
```

### upgrade

Upgrade a package.

```ini
[upgrade libxyz development package]
upgrade: libxyz-dev
```

### user

Create a user:

- `groups`: A comma separated list of groups to which the user should be added.
- `home`: The user's home directory.
- `login`: The shell to use.
- `system`: Create as a system user.

```ini
[create the deploy user]
user.add: deploy
groups: www-data
home: /var/www
```

Remove a user:

```ini
[remove bob]
user.remove: bob
```
