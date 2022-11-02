from __future__ import annotations

import os
import logging
import argparse
from pathlib import Path
from functools import lru_cache

from cookiecutter.main import cookiecutter
from cookiecutter.utils import simple_filter

if "BUILD_WORKSPACE_DIRECTORY" in os.environ:
    # we are running with bazel. This is clearly a hack, but since we
    # don't require sandbox for boostrap initial project structure, this
    # should be fine.
    _git_root = Path(os.environ["BUILD_WORKSPACE_DIRECTORY"])
else:
    _git_root = Path(__file__).parent.parent.parent

logger = logging.getLogger("bentoml")


@simple_filter
def rpart(value: str, sep: str, index: int, maxsplit: int = 1) -> str:
    v = value.rsplit(sep, maxsplit=maxsplit)
    try:
        return v[index]
    except IndexError:
        return ""


@lru_cache(maxsize=1)
def bentoml_version():
    from bentoml._internal.configuration import CLEAN_BENTOML_VERSION

    return CLEAN_BENTOML_VERSION


TEMPLATE_CHOICES = ["gen_python_packages"]

if __name__ == "__main__":
    logger.debug(f"Current working directory: {os.getcwd()}.")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "package",
        help=f"Main folder containing the contrib package. i.e: {_git_root!s}/monitoring",
    )
    parser.add_argument(
        "--parent-dir",
        type=str,
        help="whether the package has parent directory or not.",
    )
    parser.add_argument(
        "--template",
        help="template to use for the package",
        choices=TEMPLATE_CHOICES,
        default="gen_python_packages",
    )
    args = parser.parse_args()
    if args.parent_dir:
        output_path = _git_root / args.parent_dir
    else:
        output_path = _git_root
    if not output_path.exists():
        output_path.mkdir(exist_ok=True, parents=True)

    cookiecutter(
        str(_git_root / "tools" / args.template),
        output_dir=str(output_path),
        extra_context={
            "project_name": args.package,
            "bentoml_version": bentoml_version(),
            "folder": "bentoml_plugins",
            "author": "Atalaya Tech Inc.",
        },
        overwrite_if_exists=args.parent_dir is None,
    )
