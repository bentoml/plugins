load("//rules/py:python.bzl", "py_test")

package(default_visibility = ["//visibility:public"])

py_test(
    name = "package",
    args = [
        "--cov=monitoring/bentoml-plugins-arize/src",
        "--cov-report=term-missing",
    ],
    deps = ["//monitoring/bentoml-plugins-arize/src/bentoml_plugins/arize"],
)
