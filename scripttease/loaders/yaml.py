# Imports

from commonkit import parse_jinja_template, read_file
import logging
import yaml
from .base import BaseLoader

log = logging.getLogger(__name__)

# Exports

__all__ = (
    "YMLLoader",
)

# Classes


class YMLLoader(BaseLoader):

    def load(self):
        if not self.exists:
            return False

        content = self.read_file()
        if content is None:
            return False

        try:
            commands = yaml.load(content, yaml.Loader)
        except yaml.YAMLError as e:
            log.error("Failed to parse %s as a YAML file: %s" % (self.path, e))
            return False

        for command in commands:
            comment = list(command.keys())[0]
            tokens = list(command.values())[0]

            args = list()
            command_name = None
            count = 0
            kwargs = self.options.copy()
            kwargs['comment'] = comment

            for key, value in tokens.items():
                if key.startswith("_"):
                    continue

                if count == 0:
                    command_name = key

                    try:
                        if value[0] == '"':
                            args.append(value.replace('"', ""))
                        else:
                            args = value.split(" ")
                    except IndexError:
                        pass
                    except TypeError:
                        args.append(True)
                else:
                    _key, _value = self._get_key_value(key, value)
                    kwargs[_key] = _value

                count += 1

            self.snippets.append((command_name, args, kwargs))

        self.is_loaded = True

        return True
