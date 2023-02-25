load("@bazel_skylib//:bzl_library.bzl", "bzl_library")

package(default_visibility = ["//visibility:public"])

[
    bzl_library(
        name = "{}.bzl".format(src),
        srcs = ["{}.bzl".format(src)],
    )
    for src in [
        "deps",
        "workspace0",
        "workspace1",
        "workspace2",
    ]
]
