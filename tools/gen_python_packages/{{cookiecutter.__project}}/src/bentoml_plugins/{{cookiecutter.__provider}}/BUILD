load("@rules_python//python:defs.bzl", "py_library")
load("//rules/py/vendorred:pypi.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "{{ cookiecutter.__provider }}",
    srcs = ["__init__.py"],
    imports = ["../.."],
    deps = [
        requirement("bentoml"),
    ],
)
