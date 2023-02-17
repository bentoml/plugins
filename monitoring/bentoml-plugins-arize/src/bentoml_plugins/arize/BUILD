load("@rules_python//python:defs.bzl", "py_library")
load("@pypi//:requirements.bzl", plugins_requirement = "requirement")
load("@external//:requirements.bzl", external_requirement = "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "arize",
    srcs = ["__init__.py"],
    imports = ["../.."],
    deps = [
        "@com_github_bentoml_bentoml//:sdk",
        external_requirement("arize"),
        plugins_requirement("attrs"),
    ],
)

filegroup(
    name = "srcs_files",
    srcs = glob(["*.py"]) + ["py.typed"],
)
