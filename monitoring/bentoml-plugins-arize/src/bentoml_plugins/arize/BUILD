package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_library")
load("@pypi//:requirements.bzl", "requirement")

py_library(
    name = "arize",
    srcs = ["__init__.py"],
    imports = ["../.."],
    deps = [
        "@com_github_bentoml_bentoml//src/bentoml",
        requirement("arize"),
        requirement("attrs"),
    ],
)

filegroup(
    name = "srcs_files",
    srcs = glob(["*.py"]) + ["py.typed"],
)
