load("@plugins//:requirements.bzl", "requirement")
load("@com_github_bentoml_bentoml//rules/py:python.bzl", "py_test")

package(default_visibility = ["//visibility:public"])

py_test(
    name = "package",
    data = ["//monitoring/bentoml-plugins-arize/src/bentoml_plugins/arize:srcs_files"],
    deps = ["//monitoring/bentoml-plugins-arize/src/bentoml_plugins/arize"],
    starlark_requirement = requirement,
)
