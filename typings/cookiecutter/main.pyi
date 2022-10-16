from __future__ import annotations

from typing import Any

def cookiecutter(
    template: str,
    checkout: str | None = ...,
    no_input: bool = ...,
    extra_context: dict[str, Any] | None = ...,
    replay: bool = ...,
    overwrite_if_exists: bool = ...,
    output_dir: str = ...,
    config_file: str | None = ...,
    default_config: bool = ...,
    password: str | None = ...,
    directory: str | None = ...,
    skip_if_file_exists: bool = ...,
    accept_hooks: bool = ...,
) -> str: ...
