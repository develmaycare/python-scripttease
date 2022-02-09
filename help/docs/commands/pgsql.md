# PostgreSQL

Summary: Work with Postgres databases.

## Common Options

- `admin_pass`: The password off the admin-authorized user.
- `admin_user`: The user name of the admin-authorized user. Default: `postgres`
- `host`: The host name. Default: `localhost`
- `port`: The TCP port. Default: `5432`

## Available Commands

### pgsql.create

Create a database. Argument is the database name.

- `owner`: The user name that owns the database.

```ini
[create the database]
pgsql.create: database_name
```

### pgsql.drop

Drop a database. Argument is the database name.

### pgsql.dump

Dump the database schema. Argument is the database name.

- `path`: The path to the dump file. Default: `dump.sql`

### pgsql.exec

Execute an SQL statement. Argument is the SQL statement.

- `database`: The name of the database where the statement will be executed. Default: `default`

### pgsql.exists

Determine if a database exists. Argument is the database name.

### pgsql.user.create

Create a user. Argument is the user name.

- `password`: The user's password.

### pgsql.user.drop

Remove a user. Argument is the user name.

### pgsql.user.exists

Determine if a user exists. Argument is the user name.
