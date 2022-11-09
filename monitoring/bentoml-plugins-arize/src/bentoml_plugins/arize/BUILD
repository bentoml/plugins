package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_library")
load("//:requirements.bzl", "requirement")

py_library(
    name = "arize",
    srcs = ["__init__.py"],
    deps = [
        requirement("bentoml"),
        requirement("arize"),
        requirement("attrs"),
    ],
)
