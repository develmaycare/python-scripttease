# MySQL

Summary: Work with MySQL (and Maria) databases.

## Common Options

- `admin_pass`: The password off the admin-authorized user.
- `admin_user`: The user name of the admin-authorized user. Default: `root`
- `host`: The host name. Default: `localhost`
- `port`: The TCP port. Default: `3306`

## Available Commands

### mysql.create

Create a database. Argument is the database name.

- `owner`: The user name that owns the database.

```ini
[create the database]
mysql.create: database_name
```

### mysql.drop

Drop a database. Argument is the database name.

### mysql.dump

Dump the database schema. Argument is the database name.

- `path`: The path to the dump file. Default: `dump.sql`

### mysql.exec

Execute an SQL statement. Argument is the SQL statement.

- `database`: The name of the database where the statement will be executed. Default: `default`

### mysql.exists

Determine if a database exists. Argument is the database name.

### mysql.grant

Grant privileges to a user. Argument is the privileges to be granted.

- `database`: The database name where privileges are granted.
- `user`: The user name for which the privileges are provided.

### mysql.user.create

Create a user. Argument is the user name.

- `password`: The user's password.

### mysql.user.drop

Remove a user. Argument is the user name.

### mysql.user.exists

Determine if a user exists. Argument is the user name.
