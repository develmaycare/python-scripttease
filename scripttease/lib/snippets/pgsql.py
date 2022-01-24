from commonkit import parse_jinja_string


def pgsql_command_parser(snippet, args=None):
    a = list()

    if snippet.admin_pass:
        a.append('export PGPASSWORD="%s" &&' % snippet.admin_pass)

    if snippet.admin_user:
        a.append("-U %s" % snippet.admin_user)

    if snippet.host:
        a.append("--host=%s" % snippet.host)

    if snippet.port:
        a.append("--port=%s" % snippet.port)

    context = snippet.context.copy()
    context['args'] = args or snippet.args
    context.update(snippet.kwargs)

    if type(snippet.content) is list:
        b = list()
        for i in snippet.content:
            b.append(parse_jinja_string(i, context))

        return " ".join(b)

    return parse_jinja_string(snippet.content, context)


pgsql = {
    'pgsql': {
        'create': [
            '{% if admin_pass %}export PGPASSWORD="{{ admin_pass }}" &&{% endif %}',
            "createdb",
            '-U {{ admin_user|default("postgres") }}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("5432") }}',
            "{% if owner %}--owner={{ owner }}{% endif %}",
            "{% if template %}--template={{ template }}{% endif %}",
            "{{ args[0] }}",
        ],
        'drop': [
            '{% if admin_pass %}export PGPASSWORD="{{ admin_pass }}" &&{% endif %}',
            "dropdb",
            '-U {{ admin_user|default("postgres") }}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("5432") }}',
            "{{ args[0] }}",
        ],
        'dump': [
            '{% if admin_pass %}export PGPASSWORD="{{ admin_pass }}" &&{% endif %}',
            "pd_dump",
            '-U {{ admin_user|default("postgres") }}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("5432") }}',
            "--column-inserts",
            '--file={{ file_name|default("dump.sql") }}',
            "{{ args[0] }}"
        ],
        'exec': [
            '{% if admin_pass %}export PGPASSWORD="{{ admin_pass }}" &&{% endif %}',
            "psql",
            '-U {{ admin_user|default("postgres") }}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("5432") }}',
            "--dbname={{ database }}",
            '-c "{{ args[0] }}"',
        ],
        'exists': [
            '{% if admin_pass %}export PGPASSWORD="{{ admin_pass }}" &&{% endif %}',
            "psql",
            '-U {{ admin_user|default("postgres") }}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("5432") }}',
            r"-lqt | cut -d \| -f 1 | grep -qw {{ args[0] }}",
        ],
        'user': {
            'create': [
                '{% if admin_pass %}export PGPASSWORD="{{ admin_pass }}" &&{% endif %}',
                "createuser",
                '-U {{ admin_user|default("postgres") }}',
                '--host={{ host|default("localhost") }}',
                '--port={{ port|default("5432") }}',
                "-DRS {{ args[0] }}",  # no create db or roles, and not a superuser
                '{% if password %}&& psql -U {{ admin_user|default("postgres") }} '
                '--host={{ host|default("localhost") }} '
                '--port={{ port|default("5432") }} '
                ' -c "ALTER USER {{ args[0] }} WITH ENCRYPTED PASSWORD \'{{ password }}\';"'
                '{% endif %}',
            ],
            'drop': [
                '{% if admin_pass %}export PGPASSWORD="{{ admin_pass }}" &&{% endif %}',
                "dropuser",
                '-U {{ admin_user|default("postgres") }}',
                '--host={{ host|default("localhost") }}',
                '--port={{ port|default("5432") }}',
                "{{ args[0] }}"
            ],
            'exists': [
                '{% if admin_pass %}export PGPASSWORD="{{ admin_pass }}" &&{% endif %}',
                "psql",
                '-U {{ admin_user|default("postgres") }}',
                '--host={{ host|default("localhost") }}',
                '--port={{ port|default("5432") }}',
                '-c "SELECT 1 FROM pgsql_roles WHERE rolnamme={{ args[0] }};"'
            ],
        },
        # '_parser': pgsql_command_parser,
        '_register': ["exists", 'user.exists'],
    }
}

