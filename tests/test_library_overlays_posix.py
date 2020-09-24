import pytest
from scripttease.library.overlays.posix import *


def test_archive():
    c = archive(
        "/path/to/target",
        absolute=True,
        exclude="*.log",
        strip=1,
        view=True
    )
    s = c.get_statement()
    print(s)
    # tar -czPv --exclude *.log --strip-components 1 -f ./archive.tgz /path/to/target
    assert "tar -czPv --exclude *.log --strip-components 1" in s
    assert "-f ./archive.tgz /path/to/target" in s


def test_certbot():
    with pytest.raises(ValueError):
        c = certbot("example.com")

    c = certbot("example.com", email="webmaster@example.com")
    s = c.get_statement()
    assert "certbot certonly --agree-tos --email webmaster@example.com -n" in s
    assert "--webroot -w /var/www/domains/example_com/www -d example.com" in s


def test_dialog():
    c = dialog("This is a test.", title="Testing")
    s = c.get_statement(suppress_comment=True)
    # dialog --clear --backtitle "Testing" --msgbox "This is a test." 15 100; clear;
    assert 'dialog --clear --backtitle "Testing"' in s
    assert '--msgbox "This is a test." 15 100; clear;'


def test_echo():
    c = echo("This is a test.")
    s = c.get_statement(suppress_comment=True)
    assert "echo" in s
    assert "This is a test." in s


def test_extract():
    c = extract(
        "/path/to/archive.tgz",
        absolute=True,
        exclude="*.log",
        strip=1,
        view=True
    )
    s = c.get_statement()
    assert "tar -xzPv --exclude *.log --strip-components 1" in s
    assert "-f /path/to/archive.tgz ./" in s


def test_file_append():
    c = file_append("/path/to/file.txt", content="testing = yes")
    assert 'echo "testing = yes" >> /path/to/file.txt' in c.get_statement()


def test_file_copy():
    c = file_copy("/path/to/file.txt", "/path/to/new-file.txt")
    s = c.get_statement()
    assert "cp" in s
    assert "-n" in s
    assert "/path/to/file.txt /path/to/new-file.txt" in s

    c = file_copy("/path/to/dir", "/path/to/newdir", recursive=True)
    s = c.get_statement()
    assert "cp" in s
    assert "-R" in s
    assert "/path/to/dir /path/to/newdir" in s


def test_file_write():
    c = file_write("/path/to/file.txt", content="testing 123")
    assert 'echo "testing 123" > /path/to/file.txt' in c.get_statement()

    content = [
        "I am testing",
        "I am testing",
        "I am testing",
        "testing 123",
    ]
    c = file_write("/path/to/file.txt", content="\n".join(content))
    s = c.get_statement()
    assert "cat > /path/to/file.txt << EOF" in s
    assert "I am testing" in s
    assert "testing 123" in s


def test_mkdir():
    c = mkdir("/path/to/dir", mode=755, recursive=True)
    s = c.get_statement()
    assert "mkdir" in s
    assert "-m 755" in s
    assert "-p" in s
    assert "/path/to/dir" in s


def test_move():
    c = move("/path/to/file.txt", "/path/to/file.txt.b")
    assert "mv /path/to/file.txt /path/to/file.txt.b" in c.get_statement()


def test_perms():
    c = perms("/path/to/dir", group="www-data", mode=755, owner="deploy", recursive=True)
    s = c.get_statement()
    assert "chgrp -R www-data /path/to/dir" in s
    assert "chown -R deploy /path/to/dir" in s
    assert "chmod -R 755 /path/to/dir" in s


def test_prompt():
    # This is just a placeholder to test the prompt() interface. See TestPrompt.
    c = prompt("testing")
    assert isinstance(c, Prompt)


def test_remove():
    c = remove("/path/to/dir", force=True, recursive=True)
    s = c.get_statement()
    assert "rm" in s
    assert "-f" in s
    assert "-r" in s
    assert "/path/to/dir" in s


def test_rename():
    c = rename("/path/to/file.txt", "/path/to/renamed.txt")
    assert "mv /path/to/file.txt /path/to/renamed.txt" in c.get_statement()


def test_rsync():
    c = rsync(
        "/path/to/local/",
        "/path/to/remote",
        links=True,
        delete=True,
        exclude="deploy/exclude.txt",
        recursive=True,
        host="example.com",
        key_file="~/.ssh/deploy",
        user="deploy"
    )
    s = c.get_statement()
    assert "rsync --cvs-exclude --checksum --compress --copy-links --delete" in s
    assert "--exclude-from=deploy/exclude.txt" in s
    assert "-P" in s
    assert "--recursive /path/to/local/" in s
    assert '-e "ssh -i ~/.ssh/deploy -p 22"' in s
    assert "deploy@example.com:/path/to/remote" in s

    c = rsync(
        "/path/to/local/",
        "/path/to/remote",
        links=True,
        delete=True,
        exclude="deploy/exclude.txt",
        recursive=True,
    )
    s = c.get_statement()
    assert "rsync --cvs-exclude --checksum --compress --copy-links --delete" in s
    assert "--exclude-from=deploy/exclude.txt" in s
    assert "-P" in s
    assert "--recursive" in s
    assert "/path/to/local/" in s
    assert "/path/to/remote" in s


def test_scopy():
    with pytest.raises(ValueError):
        c = scopy("/path/to/local/file.txt", "/path/to/remote/file.txt")

    c = scopy(
        "/path/to/local/file.txt",
        "/path/to/remote/file.txt",
        key_file="~/.ssh/deploy",
        host="example.com",
        user="deploy"
    )
    s = c.get_statement()
    assert "scp -i ~/.ssh/deploy" in s
    assert "-P 22" in s
    assert "/path/to/local/file.txt" in s
    assert "deploy@example.com:/path/to/remote/file.txt" in s

    c = scopy(
        "/path/to/local/file.txt",
        "/path/to/remote/file.txt",
        host="example.com",
    )
    s = c.get_statement()
    assert "scp -P 22" in s
    assert "/path/to/local/file.txt" in s
    assert "example.com:/path/to/remote/file.txt" in s


def test_sed():
    c = sed("/path/to/file.txt", find="testing", replace="123")
    s = c.get_statement()
    assert "sed -i .b" in s
    assert "s/testing/123/g" in s
    assert "/path/to/file.txt" in s


def test_symlink():
    c = symlink("/var/www/domains", force=True)
    s = c.get_statement()
    assert "ln -s" in s
    assert "-f" in s
    assert "/var/www/domains" in s


def test_touch():
    c = touch("/path/to/file.txt")
    assert "touch /path/to/file.txt" in c.get_statement()


def test_wait():
    c = wait(5)
    s = c.get_statement()
    assert 'sleep 5' in s


class TestFunction(object):

    def test_to_string(self):
        f = Function("testing", comment="A test function.")
        f.commands.append(touch("/path/to/file.txt"))
        s = f.to_string()
        assert "# A test function." in s
        assert "function testing()" in s
        assert "touch /path/to/file.txt" in s


class TestPrompt(object):

    def test_init(self):
        c = Prompt("testing", choices=["yes", "no", "maybe"])
        assert type(c.choices) is list

        c = Prompt("testing", choices="yes, no, maybe")
        assert type(c.choices) is list

        c = Prompt("testing")
        assert c.choices is None

    def test_get_dialog_statement(self):
        c = Prompt("testing", choices=["yes", "no", "maybe"], fancy=True)
        s = c.get_statement()
        assert 'dialog --clear --backtitle "Input" --title "Testing"' in s
        assert '--menu "Select" 15 40 3 "yes" 1 "no" 2 "maybe" 3 2>/tmp/input.txt' in s
        assert 'testing=$(</tmp/input.txt)' in s
        assert 'clear' in s
        assert 'rm /tmp/input.txt' in s

        c = Prompt("testing", fancy=True, help_text="This is a test.")
        s = c.get_statement()
        assert 'dialog --clear --backtitle "Input" --title "Testing"' in s
        assert '--inputbox "This is a test." 8 60 2>/tmp/input.txt' in s
        assert 'testing=$(</tmp/input.txt)' in s
        assert 'clear' in s
        assert 'rm /tmp/input.txt' in s

        c = Prompt("testing", default="it is", fancy=True)
        s = c.get_statement()
        assert 'if [[ -z "$testing" ]]; then testing="it is"; fi;' in s

    def test_get_read_statement(self):
        c = Prompt("testing", choices=["yes", "no", "maybe"])
        s = c.get_statement()
        assert 'options=("yes" "no" "maybe")' in s
        assert 'select opt in "${options[@]}"' in s

        c = Prompt("testing", default="yes")
        s = c.get_statement()
        assert 'echo -n "Testing "' in s
        assert "read testing" in s
        assert 'then testing="yes"' in s
