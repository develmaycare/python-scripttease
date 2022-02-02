messages = {
    'dialog': [
        "dialog",
        "--clear",
        '--backtitle "{{ title|default("Message") }}',
        '--msgbox "{{ args[0] }}" {{ height|default("15") }} {{ width|default("100") }};'
        'clear;'
    ],
    'echo': 'echo "{{ args[0] }}"',
    'explain': None,
    'screenshot': None,
    'slack': [
        "curl -X POST -H 'Content-type: application/json' --data",
        '{"text": "{{ args[0] }}"}',
        "{{ url }}",
    ],
    'twist': [
        "curl -X POST -H 'Content-type: application/json' --data",
        '{"content": "{{ args[0] }}", "title": "{{ title|default("Notice") }}"}',
        "{{ url }}",
    ],
}