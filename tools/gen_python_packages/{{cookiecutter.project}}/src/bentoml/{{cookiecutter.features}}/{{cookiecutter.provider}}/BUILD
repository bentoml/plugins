package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_library")
load("//:requirements.bzl", "requirement")

py_library(
    {%- if cookiecutter.provider != "" %}
    name = "{{ cookiecutter.provider }}",
    {%- else %}
    name = "{{ cookiecutter.features }}",
    {%- endif %}
    srcs = ["__init__.py"],
    deps = [
        requirement("bentoml"),
    ],
)
