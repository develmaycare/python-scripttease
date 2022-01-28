posix = {
    'append': 'echo "{{ content }}" >> {{ args[0] }}',
    'archive': [
        "tar -cz",
        "{% if absolute %}-P{% endif %}",
        "{% if view %}-v{% endif %}",
        "{% if exclude %}--exclude {{ exclude }}{% endif %}",
        "{% if strip %}--strip-components {{ strip }}{% endif %}",
        "-f {{ args[0] }} {{ to }}",
    ],
    'copy': [
        "cp",
        "{% if not overwrite %}-n{% endif %}",
        "{% if recursive %}-R{% endif %}",
        "{{ args[0] }} {{ args[1] }}"
    ],
    'dir': [
        "mkdir",
        "{% if recursive %}-p{% endif %}",
        "{% if mode %}-m {{ mode }}{% endif %}",
        "{{ args[0] }}",
        "{% if group %}&& chgrp -R {{ group }} {{ args[0] }}{% endif %}",
        "{% if owner %}&& chown -R {{ owner }} {{ args[0] }}{% endif %}"
    ],
    'extract': [
        "tar",
        "-xz",
        "{% if absolute %}-P{% endif %}",
        "{% if view %}-v{% endif %}",
        "{% if exclude %}--exclude {{ exclude }}{% endif %}",
        "{% if strip %}--script-components {{ strip }}{% endif %}",
        '-f {{ args[0] }} {{ to|default("./") }}',
    ],
    'file': [
        "{% if content %}cat > {{ args[0] }} << EOF\n{{ content }}\nEOF{% else %}touch {{ args[0] }}{% endif %}",
        "{% if mode %}&& chmod {{ mode }} {{ args[0] }}{% endif %}",
        "{% if group %}&& chgrp {{ group }} {{ args[0] }}{% endif %}",
        "{% if owner %}&& chown {{ owner }} {{ args[0] }}{% endif %}"
    ],
    'link': [
        "ln -s",
        "{% if force %}-f{% endif %}",
        '{{ args[0] }} {{ args[1] }}',
    ],
    'mkdir': [
        "mkdir",
        "{% if recursive %}-p{% endif %}",
        "{% if mode %}-m {{ mode }}{% endif %}",
        "{{ args[0] }}",
        "{% if group %}&& chgrp -R {{ group }} {{ args[0] }}{% endif %}",
        "{% if owner %}&& chown -R {{ owner }} {{ args[0] }}{% endif %}"
    ],
    'move': "mv {{ args[0] }} {{ args[1] }}",
    'perms': [
        "{% if group %}chgrp {% if recursive %}-R {% endif %}{{ group }} {{ args[0] }};{% endif %}",
        "{% if mode %}chmod {% if recursive %}-R {% endif %}{{ mode }} {{ args[0] }};{% endif %}",
        "{% if owner %}chown {% if recursive %}-R {% endif %}{{ owner }} {{ args[0] }}{% endif %}",
    ],
    'push': [
        "rsync",
        "--csv-exclude",
        "--checksum",
        "--compress",
        "{% if delete %}--delete{% endif %}",
        "{% if links %}--copy-links{% endif %}",
        "{% if exclude %}--exclude-from={{ exclude }}{% endif %}",
        # --partial and --progress
        "-P",
        "{% if recursive %}--recursive{% endif %}",
        "{{ args[0] }}",
        '-e "ssh -i {{ key_file }} -p {{ port|default("22") }}',
        "{{ user }}@{{ host }}:{{ args[1] }}",
    ],
    'remove': [
        "rm",
        "{% if force %}-f{% endif %}",
        "{% if recursive %}-r{% endif %}",
        "{{ args[0] }}"
    ],
    'rename': "mv {{ args[0] }} {{ args[1] }}",
    'replace': [
        'sed -i {{ backup|default(".b") }}',
        '"s{{ delimiter|default("/") }}{{ find }}{{ delimiter|default("/") }}{{ sub }}{{ delimiter|default("/") }}g"',
        "{{ args[0] }}"
    ],
    'scopy': [
        "scp",
        "{% if key_file %}-i {{ key_file }}{% endif %}",
        '-P {{ port|default("22") }}',
        "{{ args[0] }}",
        "{{ user }}@{{ host }}:{{ args[1] }}"
    ],
    'ssl': [
        "certbot certonly",
        "--agree-tos",
        '--email {{ email|default("webmaster@" + args[0]) }}',
        "-n --webroot",
        '-w {{ webroot|default("/var/www/maint/www") }}',
        "-d {{ args[0] }}"
    ],
    'sync': [
        "rsync",
        "--csv-exclude",
        "--checksum",
        "--compress",
        "{% if delete %}--delete{% endif %}",
        "{% if links %}--copy-links{% endif %}",
        "{% if exclude %}--exclude-from={{ exclude }}{% endif %}",
        # --partial and --progress
        "-P",
        "{% if recursive %}--rescursive{% endif %}",
        "{{ args[0] }}"
        "{{ args[1] }}"
    ],
    'touch': "touch {{ args[0] }}",
    'wait': "sleep {{ args[0] }}",
    # 'write': [
    #     "cat > {{ args[0] }} << EOF",
    #     "\n",
    #     "{{ content }}",
    #     "\n",
    #     "EOF"
    # ],
    'write': "cat > {{ args[0] }} << EOF\n{{ content }}\nEOF",
}