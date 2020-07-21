apache.disable_module
.....................

.. code-block:: ini

    [disable an apache module]
    apache.disable_module = module_name

apache.disable_site
...................

.. code-block:: ini

    [disable a virtual host]
    apache.disable_site = domain_name

apache.enable_module
....................

.. code-block:: ini

    [enable an apache module]
    apache.enable_module = module_name

apache.enable_site
..................

.. code-block:: ini

    [enable a virtual host]
    apache.enable_site = domain_name

apache.test
...........

.. code-block:: ini

    [run an apache config test]
    apache: test 

append
......

.. code-block:: ini

    [append to a file]
    append = path
    content = None

archive
.......

.. code-block:: ini

    [create an archive file]
    archive = from_path
    absolute = False
    exclude = None
    file_name = archive.tgz
    strip = 0
    to_path = .
    view = False

certbot
.......

Alias: ssl

.. code-block:: ini

    [get new ssl certificate from let's encrypt]
    certbot = domain_name
    email = None
    webroot = None

copy
....

.. code-block:: ini

    [copy a file or directory]
    copy = from_path to_path
    overwrite = False
    recursive = False

django
......

.. code-block:: ini

    [run a django management command]
    django = name

django.dumpdata
...............

.. code-block:: ini

    [export django fixtures]
    django.dumpdata = app_name
    file_name = initial
    indent = 4
    natural_foreign = False
    natural_primary = False
    path = None

django.loaddata
...............

.. code-block:: ini

    [load django fixtures]
    django.loaddata = app_name
    file_name = initial
    path = None

extract
.......

.. code-block:: ini

    [extract an archive]
    extract = from_path
    absolute = False
    exclude = None
    file_name = archive.tgz
    strip = 0
    to_path = None
    view = False

install
.......

.. code-block:: ini

    [install a package using apt-get]
    apt = package
    remove = False

makedir
.......

.. code-block:: ini

    [create a directory]
    makedir = path
    mode = None
    recursive = True

message
.......

.. code-block:: ini

    [run a message command]
    message = output
    back_title = Message
    dialog = False
    height = 15
    width = 100

mkdir
.....

.. code-block:: ini

    [create a directory]
    mkdir = path
    mode = None
    recursive = True

move
....

.. code-block:: ini

    [move a file or directory]
    move = from_path to_path

perms
.....

.. code-block:: ini

    [set permissions on a file or directory]
    perms = path
    group = None
    mode = None
    owner = None
    recursive = False

pg.createdb
...........

.. code-block:: ini

    [create a postgresql database]
    pg.createdb = name
    admin_pass = None
    admin_user = postgres
    host = localhost
    owner = None
    port = 5432
    template = None

pg.createuser
.............

.. code-block:: ini

    [create a postgresql user]
    pg.createuser = name
    admin_pass = None
    admin_user = postgres
    host = localhost
    password = None
    port = 5432

pg.db
.....

.. code-block:: ini

    [create a postgresql database]
    pg.db = name
    admin_pass = None
    admin_user = postgres
    host = localhost
    owner = None
    port = 5432
    template = None

pg.dropdb
.........

.. code-block:: ini

    [remove a postgresql database]
    pg.dropdb = name
    admin_pass = None
    admin_user = postgres
    host = localhost
    port = 5432

pg.dropuser
...........

.. code-block:: ini

    [remove a postgres user]
    pg.dropuser = name
    admin_pass = None
    admin_user = postgres
    host = localhost
    port = 5432

pg.dump
.......

.. code-block:: ini

    [export a postgres database]
    pg.dump = name
    admin_pass = None
    admin_user = postgres
    file_name = None
    host = localhost
    port = 5432

pg.exists
.........

.. code-block:: ini

    [determine if a postgres database exists]
    pg.exists = name
    admin_pass = None
    admin_user = postgres
    host = localhost
    port = 5432

pip
...

.. code-block:: ini

    [install a python package using pip]
    pip = package
    remove = False
    upgrade = False

psql
....

.. code-block:: ini

    [execute a psql command]
    psql = sql
    database = template1
    host = localhost
    password = None
    port = 5432
    user = postgres

reload
......

.. code-block:: ini

    [reload a service]
    reload = service

remove
......

.. code-block:: ini

    [remove a file or directory]
    remove = path
    force = False
    recursive = False

restart
.......

.. code-block:: ini

    [restart a service]
    restart = service

rsync
.....

.. code-block:: ini

    [synchronize files from a local to remote directory]
    rsync = source target
    delete = False
    guess = False
    host = None
    key_file = None
    links = True
    port = 22
    recursive = True
    user = None

run
...

.. code-block:: ini

    [a command to be executed]
    run = statement
    comment = None
    condition = None
    cd = None
    environments = None
    function = None
    prefix = None
    register = None
    shell = None
    stop = False
    sudo = None
    tags = None

scopy
.....

.. code-block:: ini

    [copy a file from the local (machine) to the remote host]
    scp = from_path to_path
    host = None
    key_file = None
    port = 22
    user = None

sed
...

.. code-block:: ini

    [replace text in a file]
    sed = path
    backup = .b
    change = None
    delimiter = /
    find = None

start
.....

.. code-block:: ini

    [start a service]
    start = service

stop
....

.. code-block:: ini

    [stop a service]
    stop = service

symlink
.......

.. code-block:: ini

    [create a symlink]
    symlink = source
    force = False
    target = None

touch
.....

.. code-block:: ini

    [touch a file or directory]
    touch = path

virtualenv
..........

.. code-block:: ini

    [create a python virtual environment]
    virtualenv = name

write
.....

.. code-block:: ini

    [write to a file]
    write = path
    content = None
    overwrite = False
