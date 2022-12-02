package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_library")
load("@plugins//:requirements.bzl", "requirement")

py_library(
    name = "{{ cookiecutter.__provider }}",
    srcs = ["__init__.py"],
    deps = [
        requirement("bentoml"),
    ],
    imports = ["../.."]
)
