"""
Extend implementation of @rules_python//python:packaging.bzl:py_package that supports src layout and C extensions.

See https://github.com/bazelbuild/rules_python/blob/f97e00853666f1918ff58b7b2fd846791888a02d/python/private/py_package.bzl
"""

def _path_inside_wheel(f, using_src_layout = False, basedir = ""):
    # f.short_path is sometimes relative ("../${repository_root}/foobar")
    # which is not a valid path within a zip file. Fix that.
    short_path = f.short_path

    if short_path.startswith("..") and len(short_path) >= 3:
        # Path separator. '/' on linux.
        separator = short_path[2]

        # Consume '../' part.
        short_path = short_path[3:]

        # Find position of next '/' and consume everything up to that character.
        pos = short_path.find(separator)
        short_path = short_path[pos + 1:]

    if using_src_layout and short_path.startswith("src"):
        # Strip "src/" prefix from the path.
        short_path = short_path[4:]

    # Support for C extensions.
    if f.extension == "so" and basedir:
        # C extension. Move it to the root of the zip file.
        # TODO: this is wrong on Windows
        short_path = basedir + "/" + f.basename

    return short_path

def _py_package_impl(ctx):
    """
    This implementation is a hack extending the original implementation of py_package rule.
    """
    inputs = depset(
        transitive = [dep[DefaultInfo].data_runfiles.files for dep in ctx.attr.deps] +
                     [dep[DefaultInfo].default_runfiles.files for dep in ctx.attr.deps],
    )
    is_src_layout = ctx.attr.layout == "src"

    # TODO: '/' is wrong on windows, but the path separator is not available in starlark.
    # Fix this once ctx.configuration has directory separator information.
    if is_src_layout:
        # strip "src/" prefix from all packages
        packages = [p.replace(".", "/").strip("src/") for p in ctx.attr.packages]
    else:
        packages = [p.replace(".", "/") for p in ctx.attr.packages]

    if not packages:
        filtered_inputs = inputs
    else:
        filtered_files = []

        # TODO: flattening depset to list gives poor performance,
        for input_file in inputs.to_list():
            for package in packages:
                wheel_path = _path_inside_wheel(input_file, is_src_layout, package)
                if wheel_path.startswith(package):
                    if is_src_layout:
                        wheel_out = ctx.actions.declare_file(wheel_path)
                        ctx.actions.run_shell(
                            inputs = depset([input_file]),
                            outputs = [wheel_out],
                            arguments = [input_file.path, wheel_out.path],
                            command = "cp $1 $2",
                        )
                        filtered_files.append(wheel_out)
                    else:
                        filtered_files.append(input_file)
        filtered_inputs = depset(direct = filtered_files)

    return [DefaultInfo(files = filtered_inputs)]

py_package_lib = struct(
    implementation = _py_package_impl,
    attrs = {
        "deps": attr.label_list(doc = ""),
        "layout": attr.string(
            default = "adhoc",
            values = ["adhoc", "src"],
            doc = """\
The layout of the package (either 'adhoc' or 'src').
See https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#automatic-discovery
for more information.
""",
        ),
        "packages": attr.string_list(
            mandatory = False,
            allow_empty = True,
            doc = """\
List of Python packages to include in the distribution.
Sub-packages are automatically included.
""",
        ),
    },
    path_inside_wheel = _path_inside_wheel,
)
