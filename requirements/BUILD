load("@rules_python//python:pip.bzl", "compile_pip_requirements")

package(default_visibility = ["//visibility:__pkg__"])

# sets of *-requirements.in files to then be used by compile_pip_requirements
exports_files(glob(["*.txt"]))

extra_args = [
    "--allow-unsafe",
    "--resolver",
    "backtracking",
    "--no-annotate",
    "--upgrade",
    "--unsafe-package",
    "wheel",
    "--unsafe-package",
    "pip",
]

# This rule adds a convenient way to update the requirements.txt
# lockfile based on the requirements.in.
# Note that this rules will be used to distribute package with bazel.
compile_pip_requirements(
    name = "pypi",
    extra_args = extra_args,
    requirements_in = "//requirements:pypi.txt",
    requirements_txt = "//requirements:bazel-pypi.lock.txt",
    visibility = ["//visibility:__pkg__"],
)

compile_pip_requirements(
    name = "external",
    extra_args = extra_args,
    requirements_in = "//requirements:external.txt",
    requirements_txt = "//requirements:bazel-external.lock.txt",
    visibility = ["//visibility:__pkg__"],
)
