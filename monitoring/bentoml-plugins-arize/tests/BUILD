load("@pypi//:requirements.bzl", "requirement")
load("@com_github_bentoml_bentoml//rules/py:python.bzl", "py_test")

package(default_visibility = ["//visibility:public"])

py_test(
    name = "package",
    deps = ["//monitoring/bentoml-plugins-arize/src/bentoml_plugins/arize"],
)
