load("//rules/private:packaging.bzl", "py_package_lib")

py_package = rule(
    implementation = py_package_lib.implementation,
    attrs = py_package_lib.attrs,
    visibility = ["//visibility:public"],
    doc = """\
A rule to select all files in transitive dependencies of deps which
belong to given set of Python packages.
This rule is intended to be used as data dependency to py_wheel rule.
""",
)
