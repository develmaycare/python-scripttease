ubuntu = {
    'apache': {
        'disable': '{% if args[0].startswith("mod_") %}a2dismod{% else %}a2dissite{% endif %} {{ args[0] }}',
        'disable_module': "a2dissite {{ args[0] }}",
        'disable_site': "a2dismod {{ args[0] }}",
        'enable': '{% if args[0].startswith("mod_") %}a2denmod{% else %}a2ensite{% endif %} {{ args[0] }}',
        'enable_module': "a2enmod {{ args[0] }}",
        'enable_site': "a2ensite {{ args[0] }}",
        'reload': "service apache2 reload",
        'restart': "service apache2 restart",
        'start': "service apache2 start",
        'stop': "service apache2 stop",
        'test': "apachectl configtest",
    },
    'install': "apt-get install -y {{ args[0] }}",
    'reload': "service {{ args[0] }} reload",
    'restart': "service {{ args[0] }} restart",
    'run': "{{ args[0] }}",
    'start': "service {{ args[0] }} start",
    'stop': "service {{ args[0] }} stop",
    'system': {
        'reboot': "reboot",
        'update': "apt-get update -y",
        'upgrade': "apt-get upgrade -y",
    },
    'uninstall': "apt-get uninstall -y {{ args[0] }}",
    'upgrade': "apt-get install -y --only-upgrade {{ args[0] }}",
    'user': {
        # The gecos switch eliminates the prompts.
        # TODO: Deal with user password when creating a user in ubuntu.
        'create': [
            "adduser {{ args[0] }} --gecos --disabled-password",
            "{% if home %}--home {{ home }}{% endif %}",
            "{% if groups %}&& {% for group in groups %}adduser {{ args[0] }} {{ group }};{% endfor %}{% endif %}"

        ],
        'remove': "deluser {{ args[0] }}",
    },
}
