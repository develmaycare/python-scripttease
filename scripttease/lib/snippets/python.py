python = {
    'pip': [
        "{% if venv %}source {{ venv }}/bin/activate &&{%- endif %}",
        "pip{% if version %}{{ version }}{% endif %}",
        '{{ op|default("install") }}',
        '{% if op == "upgrade" %}--upgrade{% endif %}',
        "{{ args[0] }}",
    ],
    'pip3': [
        "{% if venv %}source {{ venv }}/bin/activate &&{%- endif %}",
        'pip3 {{ op|default("install") }}',
        '{% if op == "upgrade"%}--upgrade{% endif %}',
        "{{ args[0] }}",
    ],
    # 'pip': {
    #     'install': [
    #         "{% if venv %}source {{ venv }} &&{% endif %}",
    #         "{% if version %}pip{{ version }}{% else %}pip{% endif %}",
    #         "install {{ args[0] }}",
    #     ],
    #     'remove': [
    #         "{% if version %}pip{{ version }}{% else %}pip{% endif %}",
    #         "uninstall {{ args[0] }}",
    #     ],
    #     'upgrade': [
    #         "{% if version %}pip{{ version }}{% else %}pip{% endif %}",
    #         "install --upgrade {{ args[0] }}",
    #     ],
    #     '_default': "install",
    #     '_dotted': True,
    # },
    'virtualenv': "virtualenv {{ args[0] }}",
}