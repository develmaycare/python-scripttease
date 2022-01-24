from commonkit import parse_jinja_string

DJANGO_EXCLUDED_KWARGS = [
    "cd",
    "comment",
    "environments",
    "prefix",
    "register",
    "shell",
    "stop",
    "tags",
    # "venv", # ?
]

def django_command_parser(snippet, args=None, excluded_kwargs=None):

    _excluded_kwargs = excluded_kwargs or DJANGO_EXCLUDED_KWARGS

    # We need to remove the common options so any remaining keyword arguments are converted to switches for the
    # management command.
    _kwargs = snippet.kwargs.copy()
    for name in _excluded_kwargs:
        _kwargs.pop(name, None)

    # We need to remove some parameters for dumpdata and loaddata. Otherwise they end up as switches.
    if snippet.name in ("django.dumpdata", "django.loaddata"):
        app_name = _kwargs.pop("app", None)
        model_name = _kwargs.pop("model", None)

        default_path = "fixtures/%s/initial.json" % app_name
        if model_name:
            default_path = "fixtures/%s/%s.json" % (app_name, model_name.lower())

        path = _kwargs.pop("path", default_path)
        if 'path' not in snippet.kwargs:
            snippet.kwargs['path'] = path

    a = list()
    command_name = None
    for key, value in _kwargs.items():
        if key == "_name":
            command_name = value
            continue

        key = key.replace("_", "-")
        if type(value) is bool:
            if value is True:
                a.append("--%s" % key)
        else:
            a.append("--%s=%s" % (key, value))

    context = snippet.context.copy()
    context['args'] = args or snippet.args
    context['command_name'] = command_name
    context['switches'] = " ".join(a)
    context.update(snippet.kwargs)

    if type(snippet.content) is list:
        b = list()
        for i in snippet.content:
            b.append(parse_jinja_string(i, context))

        return " ".join(b)

    return parse_jinja_string(snippet.content, context)


# def django_command_builder(tokens, *args, **kwargs):
#     a = list()
#
#     command_name = tokens.pop(0)
#     if command_name == "command":
#         command_name = tokens.pop(0)
#
#     params = django_convert_params(*args, **kwargs)
#
#     a.append("./manage.py %s" % command_name)
#     if len(list(params)) > 0:
#         a.append(" ".join(list(params)))
#
#     return a
#
#
# def django_convert_params(*args, **kwargs):
#     a = list()
#     for key, value in kwargs.items():
#         key = key.replace("_", "-")
#         if type(value) is bool:
#             if value is True:
#                 a.append("--%s" % key)
#         else:
#             a.append("--%s=%s" % (key, value))
#
#     return " ".join(list(args)), " ".join(a)


django = {
    'django': {
        'check': "./manage.py check {{ switches }}",
        'command': "./manage.py {{ command_name }} {% if args %}{{ ' '.join(args) }}{% endif %} {{ switches }}",
        'dumpdata': [
            "./manage.py dumpdata {{ app }}{% if model %}.{{ model }}{% endif %}",
            # "--indent=4",
            "{{ switches }}",
            '> {{ path }}',
        ],
        'loaddata': [
            "./manage.py loaddata",
            "{{ switches }}"
            '{{ path }}',
        ],
        'migrate': "./manage.py migrate {{ switches }}",
        'static': "./manage.py collectstatic {{ switches }}",
        '_default': "command",
        '_parser': django_command_parser,
        '_prefix': "source {{ virtualenv }}/bin/activate",
        '_register': ["check", "migrate"]
    }
}
