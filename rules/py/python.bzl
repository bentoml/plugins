"""
All python-related macros and ruleset
"""

load("//rules/private:py_pytest_main.bzl", _py_pytest_main = "py_pytest_main")
load("@rules_python//python:defs.bzl", _py_test = "py_test")
load("//rules/py/vendorred:pypi.bzl", "requirement")

def py_pytest(name, args = [], data = [], **kwargs):
    """A macro that use pytest + rules_python's 'py_test'.

    This rule will create a target <name>, which will glob all 'srcs' that match 'test_<name>.py'.

    Note that if this rule will create a ":__test__" rule if given rule doesn't exist in current DAG.

    Args:
      name: The name of the test suite.
      args: Additional arguments to pass to pytest.
      data: Additional data to pass to py_test.
      **kwargs: Additional arguments to pass to py_test.
    """

    # __test__ is a special attribute from py_pytest_main
    if "__test__" not in native.existing_rules():
        _py_pytest_main(name = "__test__")

    srcs = kwargs.pop("srcs", [])
    deps = kwargs.pop("deps", [])
    env = kwargs.pop("env", {})

    if not srcs:
        srcs.append("test_{}.py".format(name))

    _py_test(
        name = name,
        srcs = [":__test__"] + srcs,
        main = ":__test__.py",
        args = ["-vvv", "-p", "no:warning"] + args,
        python_version = "PY3",
        env = env,
        deps = [
            ":__test__",
            requirement("pytest"),
            requirement("pytest-xdist"),
            requirement("pytest-asyncio"),
            requirement("build"),
            requirement("virtualenv"),
        ] + deps,
        data = data,
        legacy_create_init = 0,
        **kwargs
    )

def py_test(name, args = [], data = [], **kwargs):
    """This macro extends py_pytest to run BentoML tests.
    """
    deps = kwargs.pop("deps", [])
    py_pytest(
        name = name,
        env = {
            # NOTE: Set the following envvar to build the wheel.
            "BENTOML_BUNDLE_LOCAL_BUILD": "True",
            "SETUPTOOLS_USE_DISTUTILS": "stdlib",
        },
        args = args,
        data = ["//:pyproject"] + data,
        deps = [
            "@com_github_bentoml_bentoml//:sdk",
            requirement("pytest-cov"),
        ] + deps,
        **kwargs
    )
