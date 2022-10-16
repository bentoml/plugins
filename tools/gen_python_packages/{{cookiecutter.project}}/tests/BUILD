load("//:requirements.bzl", "requirement")
load("//bazel:python_rules.bzl", "pytest_suite")

package(default_visibility = ["//visibility:public"])

pytest_suite(
    name = "package",
    args = ["--cov={{ cookiecutter.project | replace('-', '.') }}", "--cov-report=term-missing"],
)
