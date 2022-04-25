EXCLUDED_KWARGS = [
    "cd",
    "comment",
    "condition",
    "environments",
    "name",
    "prefix",
    "register",
    "shell",
    "stop",
    "sudo",
    "tags",
]

LOGGER_NAME = "script-tease"


class PROFILE:
    """Supported operating system profiles."""

    CENTOS = "centos"
    UBUNTU = "ubuntu"
