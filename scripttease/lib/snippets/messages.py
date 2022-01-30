messages = {
    'dialog': [
        "dialog",
        "--clear",
        '--backtitle "{{ title|default("Message") }}',
        '--msgbox "{{ args[0] }}" {{ height|default("15") }} {{ width|default("100") }};'
        'clear;'
    ],
    'echo': 'echo "{{ args[0] }}"',
    'explain': "{{ args[0] }}",
    'screenshot': [
        '{% if output == "md" %}',
        "![{% if caption %}{{ caption }}]({{ args[0] }})",
        '{% elif output == "rst" %}',
        '.. figure:: {{ args[0] }}',
        '{% if caption %}\n    :alt: {{ caption }}{% endif %}',
        '{% if height %}\n    :height: {{ height }}{% endif %}',
        '{% if width %}\n    :width: {{ width }}{% endif %}'
        '\n',
        '{% else %}',
        '<img src="{{ args[0] }}"{% if caption %} alt="{{ caption }}{% endif %}'
        '{% if classes %} class={{ classes }}{% endif %}'
        '{% if height %} height="{{ height }}{% endif %}{% if width %} width="{{ width }}"{% endif %}>',
        '{% endif %}',
    ],
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