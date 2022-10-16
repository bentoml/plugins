from __future__ import annotations

from typing import Any
from typing import Callable

from jinja2.ext import Extension

_F = Callable[..., Any]

def simple_filter(filter_function: _F) -> Extension: ...
