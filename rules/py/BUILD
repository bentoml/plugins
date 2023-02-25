load("@rules_python//python:defs.bzl", "py_binary")
load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//rules/py/vendorred:pypi.bzl", "requirement")

package(default_visibility = ["//:__subpackages__"])

exports_files(["*.py"])

bzl_library(
    name = "python.bzl",
    srcs = ["python.bzl"],
)

py_binary(
    name = "flake8",
    testonly = True,
    srcs = ["_flake8_wrapper.py"],
    main = "_flake8_wrapper.py",
    visibility = ["//visibility:public"],
    deps = [
        requirement("flake8"),
        requirement("flake8-quotes"),
        requirement("flake8-pyproject"),
    ],
)
