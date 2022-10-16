load("@rules_python//python:defs.bzl", "py_test")
load("//:requirements.bzl", "requirement")

def pytest_suite(name, srcs = None, deps = [], args = [], data = [], **kwargs):
    """A test suite rule that use pytest to run Python tests.

    This rule will create a target <name>.native, which will glob all 'srcs' that match 'test_<name>.py'.

        bazel test //dir:package.native

    Args:
      name: The name of the test suite.
      **kwargs: Additional arguments to pass to py_test.
    """
    if srcs == None:
        srcs = ["test_{}.py".format(name)]
    py_test(
        name = "{}.native".format(name),
        srcs = ["//bazel:_pytest_wrapper.py"] + srcs,
        main = "//bazel:_pytest_wrapper.py",
        args = [
            "-c=$(location //:pyproject)",
        ] + args + ["$(location :%s)" % src for src in srcs],
        python_version = "PY3",
        deps = deps + [
            requirement("pytest"),
            requirement("pytest-cov"),
            requirement("pytest-xdist"),
            requirement("pytest-asyncio"),
            requirement("bentoml"),
        ],
        data = [
            "//:pyproject",
        ] + data,
        **kwargs
    )
