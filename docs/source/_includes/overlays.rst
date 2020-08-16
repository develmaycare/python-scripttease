Common
======

Common commands are available to all overlays.

pip
---

Use pip to install or uninstall a Python package.

- name (str): The name of the package.
- op (str): The operation to perform; install, uninstall
- upgrade (bool): Upgrade an installed package.
- venv (str): The name of the virtual environment to load.


.. code-block:: ini

    [run pip command]
    pip: name
    op: install
    upgrade: False
    venv: None

run
---

Run any statement.

- statement (str): The statement to be executed.


.. code-block:: ini

    [run run command]
    run: statement

virtualenv
----------

Create a Python virtual environment.

- name (str): The name of the environment to create.


.. code-block:: ini

    [run virtualenv command]
    virtualenv: name

Django
======

Django commands are available to all overlays.

django
------

Run any Django management command.

- name (str): The name of the management command.
- venv (str): The of the virtual environment to use.

args are passed as positional arguments, while kwargs are given as switches.


.. code-block:: ini

    [run django command]
    django: name args
    venv: None

django.check
------------

Run the Django check command.

- venv (str): The of the virtual environment to use.


.. code-block:: ini

    [run django.check command]
    django.check: 
    venv: None

django.collect_static
---------------------

Collect static files.

- venv (str): The of the virtual environment to use.


.. code-block:: ini

    [run django.collect_static command]
    django.collect_static: 
    venv: None

django.dumpdata
---------------

Dump data from the database.

- app_name (str): The name (app label) of the app. ``app_label.ModelName`` may also be given.
- base_path (str): The path under which apps are located in source.
- file_name (str): The file name to which the data will be dumped.
- indent (int): Indentation of the exported fixtures.
- natural_foreign (bool): Use the natural foreign parameter.
- natural_primary (bool): Use the natural primary parameter.
- path (str): The path to the data file.
- venv (str): The of the virtual environment to use.


.. code-block:: ini

    [run django.dumpdata command]
    django.dumpdata: app_name
    base_path: local
    file_name: initial
    indent: 4
    natural_foreign: False
    natural_primary: False
    path: None
    venv: None

django.loaddata
---------------

Load data into the database.

- app_name (str): The name (app label) of the app. ``app_label.ModelName`` may also be given.
- base_path (str): The path under which apps are located in source.
- file_name (str): The file name to which the data will be dumped.
- path (str): The path to the data file.
- venv (str): The of the virtual environment to use.


.. code-block:: ini

    [run django.loaddata command]
    django.loaddata: app_name
    base_path: local
    file_name: initial
    path: None
    venv: None

django.migrate
--------------

Apply database migrations.

- venv (str): The of the virtual environment to use.


.. code-block:: ini

    [run django.migrate command]
    django.migrate: 
    venv: None

Postgres
========

Postgres commands.

pg.client
---------

Execute a psql command.

- sql (str): The SQL to be executed.
- database (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.client command]
    pg.client: sql
    database: template1
    host: localhost
    password: None
    port: 5432
    user: postgres

pg.createdatabase
-----------------

Create a PostgreSQL database.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- owner (str): The owner (user/role name) of the new database.
- port (int): The port number of the Postgres service running on the host.
- template (str): The database template name to use, if any.


.. code-block:: ini

    [run pg.createdatabase command]
    pg.createdatabase: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    owner: None
    port: 5432
    template: None

pg.createdb
-----------

Create a PostgreSQL database.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- owner (str): The owner (user/role name) of the new database.
- port (int): The port number of the Postgres service running on the host.
- template (str): The database template name to use, if any.


.. code-block:: ini

    [run pg.createdb command]
    pg.createdb: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    owner: None
    port: 5432
    template: None

pg.createuser
-------------

Create a PostgreSQL user.

- name (str): The user name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.createuser command]
    pg.createuser: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    password: None
    port: 5432

pg.database
-----------

Create a PostgreSQL database.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- owner (str): The owner (user/role name) of the new database.
- port (int): The port number of the Postgres service running on the host.
- template (str): The database template name to use, if any.


.. code-block:: ini

    [run pg.database command]
    pg.database: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    owner: None
    port: 5432
    template: None

pg.database_exists
------------------

Determine if a Postgres database exists.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- owner (str): The owner (user/role name) of the new database.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.database_exists command]
    pg.database_exists: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    port: 5432

pg.db
-----

Create a PostgreSQL database.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- owner (str): The owner (user/role name) of the new database.
- port (int): The port number of the Postgres service running on the host.
- template (str): The database template name to use, if any.


.. code-block:: ini

    [run pg.db command]
    pg.db: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    owner: None
    port: 5432
    template: None

pg.dropdatabase
---------------

Remove a PostgreSQL database.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.dropdatabase command]
    pg.dropdatabase: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    port: 5432

pg.dropdb
---------

Remove a PostgreSQL database.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.dropdb command]
    pg.dropdb: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    port: 5432

pg.dropuser
-----------

Remove a Postgres user.

- name (str): The user name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.dropuser command]
    pg.dropuser: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    port: 5432

pg.dump
-------

Export a Postgres database.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- file_name (str): The name/path of the export file. Defaults the database name plus ``.sql``.
- host (str): The database host name or IP address.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.dump command]
    pg.dump: name
    admin_pass: None
    admin_user: postgres
    file_name: None
    host: localhost
    port: 5432

pg.dumpdb
---------

Export a Postgres database.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- file_name (str): The name/path of the export file. Defaults the database name plus ``.sql``.
- host (str): The database host name or IP address.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.dumpdb command]
    pg.dumpdb: name
    admin_pass: None
    admin_user: postgres
    file_name: None
    host: localhost
    port: 5432

pg.exists
---------

Determine if a Postgres database exists.

- name (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- owner (str): The owner (user/role name) of the new database.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.exists command]
    pg.exists: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    port: 5432

pg.user
-------

Create a PostgreSQL user.

- name (str): The user name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run pg.user command]
    pg.user: name
    admin_pass: None
    admin_user: postgres
    host: localhost
    password: None
    port: 5432

psql
----

Execute a psql command.

- sql (str): The SQL to be executed.
- database (str): The database name.
- admin_pass (str): The password for the user with sufficient access privileges to execute the command.
- admin_user (str): The name of the user with sufficient access privileges to execute the command.
- host (str): The database host name or IP address.
- port (int): The port number of the Postgres service running on the host.


.. code-block:: ini

    [run psql command]
    psql: sql
    database: template1
    host: localhost
    password: None
    port: 5432
    user: postgres

POSIX
=====

Posix commands form the basis of overlays for nix platforms.

append
------

Append content to a file.

- path (str): The path to the file.
- content (str): The content to be appended.


.. code-block:: ini

    [run append command]
    append: path
    content: None

archive
-------

Create a file archive.

- from_path (str): The path that should be archived.
- absolute (bool): Set to ``True`` to preserve the leading slash.
- exclude (str): A pattern to be excluded from the archive.
- strip (int): Remove the specified number of leading elements from the path.
- to_path (str): Where the archive should be created. This should *not* include the file name.
- view (bool): View the output of the command as it happens.


.. code-block:: ini

    [run archive command]
    archive: from_path
    absolute: False
    exclude: None
    file_name: archive.tgz
    strip: None
    to_path: .
    view: False

certbot
-------

Get new SSL certificate from Let's Encrypt.

- domain_name (str): The domain name for which the SSL certificate is requested.
- email (str): The email address of the requester sent to the certificate authority. Required.
- webroot (str): The directory where the challenge file will be created.


.. code-block:: ini

    [run certbot command]
    certbot: domain_name
    email: None
    webroot: None

copy
----

Copy a file or directory.

- from_path (str): The file or directory to be copied.
- to_path (str): The location to which the file or directory should be copied.
- overwrite (bool): Indicates files and directories should be overwritten if they exist.
- recursive (bool): Copy sub-directories.


.. code-block:: ini

    [run copy command]
    copy: from_path to_path
    overwrite: False
    recursive: False

extract
-------

Extract a file archive.

- from_path (str): The path that should be archived.
- absolute (bool): Set to ``True`` to preserve the leading slash.
- exclude (str): A pattern to be excluded from the archive.
- strip (int): Remove the specified number of leading elements from the path.
- to_path (str): Where the archive should be extracted. This should *not* include the file name.
- view (bool): View the output of the command as it happens.


.. code-block:: ini

    [run extract command]
    extract: from_path
    absolute: False
    exclude: None
    strip: None
    to_path: None
    view: False

func
----

A function that may be used to organize related commands to be called together.
.. code-block:: ini

    [run func command]
    func: name
    commands: None
    comment: None

mkdir
-----

Create a directory.

- path (str): The path to be created.
- mode (int | str): The access permissions of the new directory.
- recursive (bool): Create all directories along the path.


.. code-block:: ini

    [run mkdir command]
    mkdir: path
    mode: None
    recursive: True

move
----

Move a file or directory.

- from_path (str): The current path.
- to_path (str): The new path.


.. code-block:: ini

    [run move command]
    move: from_path to_path

perms
-----

Set permissions on a file or directory.

- path (str): The path to be changed.
- group (str): The name of the group to be applied.
- mode (int | str): The access permissions of the file or directory.
- owner (str): The name of the user to be applied.
- recursive: Create all directories along the path.


.. code-block:: ini

    [run perms command]
    perms: path
    group: None
    mode: None
    owner: None
    recursive: False

remove
------

Remove a file or directory.

- path (str): The path to be removed.
- force (bool): Force the removal.
- recursive (bool): Remove all directories along the path.


.. code-block:: ini

    [run remove command]
    remove: path
    force: False
    recursive: False

rename
------

Rename a file or directory.

- from_name (str): The name (or path) of the existing file.
- to_name (str): The name (or path) of the new file.


.. code-block:: ini

    [run rename command]
    rename: from_name to_name

rsync
-----

Synchronize a directory structure.

- source (str): The source directory.
- target (str): The target directory.
- delete (bool): Indicates target files that exist in source but not in target should be removed.
- exclude (str): The path to an exclude file.
- host (str): The host name or IP address. This causes the command to run over SSH.
- key_file (str): The privacy SSH key (path) for remote connections. User expansion is automatically applied.
- links (bool): Include symlinks in the sync.
- port (int): The SSH port to use for remote connections.
- recursive (bool): Indicates source contents should be recursively synchronized.
- user (str): The user name to use for remote connections.


.. code-block:: ini

    [run rsync command]
    rsync: source target
    delete: False
    exclude: None
    host: None
    key_file: None
    links: True
    port: 22
    recursive: True
    user: None

scopy
-----

Copy a file or directory to a remote server.

- from_path (str): The source directory.
- to_path (str): The target directory.
- host (str): The host name or IP address. Required.
- key_file (str): The privacy SSH key (path) for remote connections. User expansion is automatically applied.
- port (int): The SSH port to use for remote connections.
- user (str): The user name to use for remote connections.


.. code-block:: ini

    [run scopy command]
    scopy: from_path to_path
    host: None
    key_file: None
    port: 22
    user: None

sed
---

Find and replace text in a file.

- path (str): The path to the file to be edited.
- backup (str): The backup file extension to use.
- delimiter (str): The pattern delimiter.
- find (str): The old text. Required.
- replace (str): The new text. Required.


.. code-block:: ini

    [run sed command]
    sed: path
    backup: .b
    delimiter: /
    find: None
    replace: None

ssl
---

Get new SSL certificate from Let's Encrypt.

- domain_name (str): The domain name for which the SSL certificate is requested.
- email (str): The email address of the requester sent to the certificate authority. Required.
- webroot (str): The directory where the challenge file will be created.


.. code-block:: ini

    [run ssl command]
    ssl: domain_name
    email: None
    webroot: None

symlink
-------

Create a symlink.

- source (str): The source of the link.
- force (bool): Force the creation of the link.
- target (str): The name or path of the target. Defaults to the base name of the source path.


.. code-block:: ini

    [run symlink command]
    symlink: source
    force: False
    target: None

touch
-----

Touch a file or directory.

- path (str): The file or directory to touch.


.. code-block:: ini

    [run touch command]
    touch: path

write
-----

Write to a file.

- path (str): The file to be written.
- content (str): The content to be written. Note: If omitted, this command is equivalent to ``touch``.


.. code-block:: ini

    [run write command]
    write: path
    content: None

Cent OS
=======

The Cent OS overlay incorporates commands specific to that platform as well as commands from common, Django, Postgres, and POSIX.

apache
------

Execute an Apache-related command.

- op (str): The operation to perform; reload, restart, start, stop, test.


.. code-block:: ini

    [run apache command]
    apache: op

install
-------

Install a system-level package.

- name (str): The name of the package to install.


.. code-block:: ini

    [run install command]
    install: name

reload
------

Reload a service.

- name (str): The service name.


.. code-block:: ini

    [run reload command]
    reload: name

restart
-------

Restart a service.

- name (str): The service name.


.. code-block:: ini

    [run restart command]
    restart: name

start
-----

Start a service.

- name (str): The service name.


.. code-block:: ini

    [run start command]
    start: name

stop
----

Stop a service.

- name (str): The service name.


.. code-block:: ini

    [run stop command]
    stop: name

system
------

Perform a system operation.

- op (str): The operation to perform; reboot, update, upgrade.


.. code-block:: ini

    [run system command]
    system: op

template
--------

Create a file from a template.

- source (str): The path to the template file.
- target (str): The path to where the new file should be created.
- backup (bool): Indicates whether a backup should be made if the target file already exists.
- parser (str): The parser to use ``jinja`` (the default) or ``simple``.


.. code-block:: ini

    [run template command]
    template: source target
    backup: True
    parser: None

uninstall
---------

Uninstall a system-level package.

- name (str): The name of the package to uninstall.


.. code-block:: ini

    [run uninstall command]
    uninstall: name

user
----

Create or remove a user.

- name (str): The user name.
- groups (str | list): A list of groups to which the user should belong.
- home (str): The path to the user's home directory.
- op (str); The operation to perform; ``add`` or ``remove``.
- password (str): The user's password. (NOT IMPLEMENTED)


.. code-block:: ini

    [run user command]
    user: name
    groups: None
    home: None
    op: add
    password: None

Ubuntu
======

The Ubuntu overlay incorporates commands specific to that platform as well as commands from common, Django, Postgres, and POSIX.

apache
------

Execute an Apache-related command.

- op (str): The operation to perform; reload, restart, start, stop, test.


.. code-block:: ini

    [run apache command]
    apache: op

apache.disable_module
---------------------

Disable an Apache module.

- name (str): The module name.


.. code-block:: ini

    [run apache.disable_module command]
    apache.disable_module: name

apache.disable_site
-------------------

Disable an Apache site.

- name (str): The domain name.


.. code-block:: ini

    [run apache.disable_site command]
    apache.disable_site: name

apache.enable_module
--------------------

Enable an Apache module.

- name (str): The module name.


.. code-block:: ini

    [run apache.enable_module command]
    apache.enable_module: name

apache.enable_site
------------------

Enable an Apache site.



.. code-block:: ini

    [run apache.enable_site command]
    apache.enable_site: name

install
-------

Install a system-level package.

- name (str): The name of the package to install.


.. code-block:: ini

    [run install command]
    install: name

reload
------

Reload a service.

- name (str): The service name.


.. code-block:: ini

    [run reload command]
    reload: name

restart
-------

Restart a service.

- name (str): The service name.


.. code-block:: ini

    [run restart command]
    restart: name

start
-----

Start a service.

- name (str): The service name.


.. code-block:: ini

    [run start command]
    start: name

stop
----

Stop a service.

- name (str): The service name.


.. code-block:: ini

    [run stop command]
    stop: name

system
------

Perform a system operation.

- op (str): The operation to perform; reboot, update, upgrade.


.. code-block:: ini

    [run system command]
    system: op

template
--------

Create a file from a template.

- source (str): The path to the template file.
- target (str): The path to where the new file should be created.
- backup (bool): Indicates whether a backup should be made if the target file already exists.
- parser (str): The parser to use ``jinja`` (the default) or ``simple``.


.. code-block:: ini

    [run template command]
    template: source target
    backup: True
    parser: None

uninstall
---------

Uninstall a system-level package.

- name (str): The name of the package to uninstall.


.. code-block:: ini

    [run uninstall command]
    uninstall: name

user
----

Create or remove a user.

- name (str): The user name.
- groups (str | list): A list of groups to which the user should belong.
- home (str): The path to the user's home directory.
- op (str); The operation to perform; ``add`` or ``remove``.
- password (str): The user's password. (NOT IMPLEMENTED)


.. code-block:: ini

    [run user command]
    user: name
    groups: None
    home: None
    op: add
    password: None

