load("@rules_python//python:defs.bzl", "py_binary")
load("//rules/py/vendorred:pypi.bzl", "requirement")

py_binary(
    name = "bootstrap",
    srcs = ["//tools/gen_python_packages:bootstrap.py"],
    deps = [
        requirement("bentoml"),
        requirement("cookiecutter"),
    ],
)
