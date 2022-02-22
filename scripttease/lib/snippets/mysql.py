mysql = {
    'mysql': {
        'create': [
            "mysqladmin create",
            '--user={{ admin_user|default("root") }}',
            '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("3306") }}',
            "{{ args[0] }}",
            '{% if owner %}&& mysql --user {{ admin_user|default("root") }} '
            '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %} '
            '--host={{ host|default("localhost") }} '
            '--port={{ port|default("3306") }} '
            '--execute="GRANT ALL ON {{ args[0] }}.* TO \'{{ owner }}\'@\'{{ host|default("localhost") }}\'"'
            '{% endif %}'
        ],
        'drop': [
            "mysqladmin drop",
            '--user={{ admin_user|default("root") }}',
            '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("3306") }}',
            "{{ args[0] }}",
        ],
        'dump': [
            "mysqldump",
            '--user={{ admin_user|default("root") }}',
            '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("3306") }}',
            '--complete-inserts',
            '{{ args[0] }} > {{ path|default("dump.sql") }}',
        ],
        'exec': [
            "mysql",
            '--user={{ admin_user|default("root") }}',
            '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("3306") }}',
            '--execute="{{ args[0] }}"',
            '{{ database|default("default") }}',
        ],
        'exists': [
            "mysql",
            '--user={{ admin_user|default("root") }}',
            '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("3306") }}',
            '--execute="SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = \'{{ args[0] }}\'"',
        ],
        'grant': [
            "mysql",
            '--user={{ admin_user|default("root") }}',
            '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %}',
            '--host={{ host|default("localhost") }}',
            '--port={{ port|default("3306") }}',
            '--execute="GRANT {{ args[0] }} ON {{ database|default("default") }}.* TO \'{{ user }}\'@\'{{ host|default("localhost") }}\'"'
        ],
        'user': {
            'create': [
                "mysql",
                '--user={{ admin_user|default("root") }}',
                '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %}',
                '--host={{ host|default("localhost") }}',
                '--port={{ port|default("3306") }}',
                '--execute="CREATE USER IF NOT EXISTS \'{{ args[0] }}\'@\'{{ host|default("localhost") }}\'" '
                '{% if password %}IDENTIFIED BY PASSWORD(\'{{ password }}\'{% endif %}'
            ],
            'drop': [
                "mysql",
                '--user={{ admin_user|default("root") }}',
                '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %}',
                '--host={{ host|default("localhost") }}',
                '--port={{ port|default("3306") }}',
                '--execute="DROP USER IF EXISTS \'{{ args[0] }}\'@\'{{ host|default("localhost") }}\'"'
            ],
            'exists': [
                "mysql",
                '--user={{ admin_user|default("root") }}',
                '{% if admin_pass %}--password="{{ admin_pass }}"{% endif %}',
                '--host={{ host|default("localhost") }}',
                '--port={{ port|default("3306") }}',
                '--execute="SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = \'{{ args[0] }}\')"'
            ],
        },
    }
}
