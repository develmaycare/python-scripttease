# Messages

Summary: Send feedback to users.

## Available Commands

### dialog

Use the dialog CLI to display a message.

- `height`: The height of the dialog box. Default: `15`
- `title`: An optional title to display as part of the dialog box. Default: `Message`.
- `width`: The width of the dialog box. Default: `100`

```ini
[send some feedback]
dialog: "This is a message."
```

```yaml
- send some feedback:
  dialog: "This is a message."
```

!!! warning

    The dialog command line utility must be installed.

### explain

Provide an explanation. When generating code this is added as a comment. When documentation is generated, it is output as text.

```ini
[introduction]
explain: "These steps will set up a Radicale CalDav/CardDav server."
header: Introduction
```

The `header` option is not used in comments, but makes documentation more readable and facilitates the creation of tutorials or install guides that re-use the defined steps.

### echo

Display a simple message.

```ini
[send some feedback]
echo: "This is a message."
```

```yaml
- send some feedback:
  echo: "This is a message."
```

### slack

Send a message via Slack.

- `url`: Required. The URL to which the message should be sent.

```ini
[send some feedback]
slack: "This is a message."
url: https://subdomain.slack.com/path/to/your/integration
```

```yaml
- send some feedback:
  slack: "This is a message."
  url: https://subdomain.slack.com/path/to/your/integration
```

!!! note
    You could easily define a variable for the Slack URL and set ``url: {{ slack_url }}`` to save some typing. See [variables](../config/variables.md).

### screenshot

Like `explain` above, a screenshot adds detail to comments or documentation, but does not produce a command statement.

```ini
[login screenshot after successful install]
screenshot: images/login.png
caption: Login Page
height: 50%
width: 50%
```

The value of `screenshot` may be relative to the command file or a full URL to the image. If `caption` is omitted the section (comment) is used.

### twist

Send a message via [Twist](https://twist.com).

- `title`: The title of the message. Default: `Notice`
- `url`: Required. The URL to which the message should be sent.

```ini
[send some feedback]
twist: "This is a message."
url: https://subdomain.twist.com/path/to/your/integration
```

```yaml
- send some feedback:
  twist: "This is a message."
  url: https://subdomain.twist.com/path/to/your/integration
```

!!! note

    As with Slack, you could easily define a variable for the Twist URL and set ``url: {{ twist_url }}``. See [variables](../config/variables.md).
