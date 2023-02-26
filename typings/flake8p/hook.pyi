import typing as t
import configparser

from flake8.options.manager import OptionManager

flake8_parse_config: t.Callable[
    [OptionManager, configparser.RawConfigParser, str], dict[str, t.Any]
] = ...

def parse_config(
    option_manager: OptionManager, cfg: configparser.RawConfigParser, cfg_dir: str
) -> dict[str, t.Any]:
    """
    Overrides Flake8's configuration parsing.

    If we discover `pyproject.toml` in the current folder, we discard
    anything that may have been read from whatever other configuration
    file and read the `tool.flake8` section in `pyproject.toml` instead.

    If a custom TOML file was specified via the `--toml-config`
    command-line option, we read the section from that file instead.
    """
    ...

class Plugin:
    """
    Installs the hook when called via `flake8` itself.

    Also adds the command-line option `--toml-config` to Flake8.
    """

    @classmethod
    def add_options(cls, parser: configparser.RawConfigParser): ...

def main(argv: t.Sequence[str] | None = None) -> int: ...
