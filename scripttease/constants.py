import os

__all__ = (
    "LOGGER_NAME",
    "PATH_TO_SCRIPT_TEASE",
)

LOGGER_NAME = "script-tease"

PATH_TO_SCRIPT_TEASE = os.path.abspath(os.path.dirname(__file__))
