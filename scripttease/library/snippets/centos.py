centos = {
    'apache': {
        'reload': "apachectl -k reload",
        'restart': "apachectl -k restart",
        'start': "apachectl -k start",
        'stop': "apachectl -k stop",
        'test': "apachectl configtest",
    },
    'install': "yum install -y {{ args[0] }}",
    'reload': "systemctl reload {{ args[0] }}",
    'restart': "systemctl restart {{ args[0] }}",
    'start': "systemctl start {{ args[0] }}",
    'stop': "systemctl stop {{ args[0] }}",
    'system': {
        'reboot': "reboot",
        'update': "yum check-update",
        'upgrade': "yum update -y",
    },
    'uninstall': "yum remove -y {{ args[0] }}",
    'user': {
        'create': [
            "adduser {{ args[0] }}",
            "{% if home %}--home {{ home }}{% endif %}",
            "{% if groups %}&& {% for group in groups %}gpasswd -a {{ args[0] }} {{ group }};{% endfor %}{% endif %}"
        ],
        'remove': "userdel -r {{ args[0] }}",
    }
}
