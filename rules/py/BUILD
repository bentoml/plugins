load("@rules_python//python:defs.bzl", "py_library")
load("@plugins//:requirements.bzl", "requirement")

package(default_visibility = ["//:__subpackges__"])

exports_files(["*.py"])

py_binary(
    name = "flake8",
    testonly = True,
    srcs = ["run_flake.py"],
    visibility = ["//visibility:public"],
    deps = [
        requirement("flake8"),
        requirement("flake8-quotes"),
        requirement("flake8-pyproject"),
    ],
)
