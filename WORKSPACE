workspace(name = "com_github_bentoml_plugins")

load("//rules:deps.bzl", "internal_deps")

internal_deps()

load("//rules:workspace0.bzl", "workspace0")

workspace0()

load("//rules:workspace1.bzl", "workspace1")

workspace1()

load("//rules:workspace2.bzl", "workspace2")

workspace2()

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

python_register_toolchains(
    name = "python3_10",
    python_version = "3.10",
)

load("@python3_10//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_parse")

# NOTE: pypi requirements to load its py_test rules
pip_parse(
    name = "pypi",
    python_interpreter_target = interpreter,
    requirements_lock = "//requirements:bazel-pypi.lock.txt",
)

load("@pypi//:requirements.bzl", "install_deps")

install_deps()
