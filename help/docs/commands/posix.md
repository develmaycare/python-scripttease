# POSIX

Summary: Work with common POSIX-compliant commands..

## Available Commands

### append

Append content to a file. Argument is the file name.

- `content`: The content to be appended.

### archive

Create an archive (tarball). Argument is the target file or directory.

- `absolute`: Don't strip leading slashes from file names.
- `view`: View the progress.
- `exclude`: Exclude file name patterns.
- `strip`: Strip component paths to the given depth (integer).
- `to`: The path to where the archive will be created.

### copy

Copy a file or directory. First argument is the target file/directory. Second argument is the destination.

- `overwrite`: Overwrite an existing target.
- `recursive`: Copy directories recursively.

### dir

Create a directory. Argument is the path.

- `group`: Set the group to the given group name.
- `mode`: Set the mode on the path.
- `owner`: Set the owner to the given owner name.
- `recursive`: Create the full path even if intermediate directories do not exist.

### extract

Extract an archive (tarball). Argument is the path to the archive file.

- `absolute`: Strip leading slashes from file names.
- `view`: View the progress.
- `exclude`: Exclude file name patterns.
- `strip`: Strip component paths to the given depth (integer).
- `to`: The path to where the archive will be extracted. Defaults to the current working directory.

### file

Create a file. Argument is the path.

- `content`: The content of the file. Otherwise, an empty file is created.
- `group`: Set the group to the given group name.
- `mode`: Set the mode on the path.
- `owner`: Set the owner to the given owner name.

### link

Create a symlink. First argument is the target. Second argument is the destination.

- `force`: Force creation of the link.

### move

Move a file or directory. First argument is the target. Second argument is the desitnation.

### perms

Set permissions on a file or directory. Argument is the path.

- `group`: Set the group to the given group name.
- `mode`: Set the mode on the path.
- `owner`: Set the owner to the given owner name.
- `recursive`: Apply permission recursively (directories only).

### push

Push (rsync) a path to a remote server. First argument is the local path. Second argument is the remote path.

- `delete`: Delete existing files/directories.
- `host`: The host name. Required.
- `key_file`: Use the given SSL (private) key. Required.
- `links`: Copy symlinks.
- `exclude`: Exclude patterns from the given (local) file.
- `port`: The TCP port on the host. Default: `22`
- `recursive`: Operate recursively on directories.
- `user`: The user name. Required.

### remove

Remove a file or directory. Argument is the path.

- `force`: Force the removal.
- `recursive`: Remove (directories) rescurisvely.

### rename

Rename a file or directory. First argument is the target. Second argument is the destination.

### replace

Replace something in a file. First argument is the path.

- `backup`: Create a backup.
- `delimiiter`: The sed delimiter. Default: `/`
- `find`: The text to be found. Required.
- `sub`: The text to be replaced. Required.

### scopy

Copy a file to a remote server. First argument is the local file name. Second argument is the remote destination.

- `key_file`: The private key file to use for the connection.
- `host`: The host name. Required.
- `port`: The TCP port. Default: `22`
- `user`: The user name. Required.

### ssl

Use Let's Encrypt (certbot) to acquire an SSL certificate. Argument is the domain name.

- `email`: The email address for "agree tos". Default: `webmaster@domain_name`
- `webroot`: The webroot to use. Default: `/var/www/maint/www`

### sync

Sync (rsync) local files and directories. First argument is the target. Second argument is the destination.

- `delete`: Delete existing files/directories.
- `links`: Copy symlinks.
- `exclude`: Exclude patterns from the given (local) file.
- `recursive`: Operate recursively on directories.

### touch

Touch a file, whether it exists or not. Argument is the path.

### wait

Wait for n number of seconds before continuing. Argument is the number of seconds.

### write

Write to a file. Argument is the path.

- `content`: The content to write to the file. Replaces existing content.

