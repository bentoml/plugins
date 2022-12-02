load("@rules_python//python:defs.bzl", _py_library = "py_library", _py_test = "py_test")
load("@aspect_rules_py//py:defs.bzl", _pytest_main = "py_pytest_main")
load("@pypi//:requirements.bzl", "requirement")

def py_test(name, args = [], data = [], **kwargs):
    # sync with bentoml/bentoml/tree/main/rules/py/python.bzl

    # __test__ is a special attribute from py_pytest_main
    if "__test__" not in native.existing_rules():
        _pytest_main(name = "__test__")

    srcs = kwargs.pop("srcs", [])
    deps = kwargs.pop("deps", [])

    if not srcs:
        srcs += ["test_{}.py".format(name)]

    _py_test(
        name = name,
        srcs = [":__test__"] + srcs,
        main = ":__test__.py",
        args = ["-vvv", "-p", "no:warning"] + args,
        python_version = "PY3",
        env = {
            # NOTE: Set the following envvar to build the wheel.
            "BENTOML_BUNDLE_LOCAL_BUILD": "True",
            "SETUPTOOLS_USE_DISTUTILS": "stdlib",
        },
        deps = [
            ":__test__",
            "@com_github_bentoml_bentoml//:sdk",
            "@com_github_bentoml_bentoml//:cli",
            requirement("pytest"),
            requirement("pytest-xdist"),
            requirement("pytest-asyncio"),
            requirement("build"),
            requirement("virtualenv"),
        ] + deps,
        data = ["//:pyproject"] + data,
        legacy_create_init = 0,
        **kwargs
    )
