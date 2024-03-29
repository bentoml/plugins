# Vendored from aspect-build/rules_py
load("@rules_python//python:defs.bzl", _py_library = "py_library")

def _py_pytest_main_impl(ctx):
    substitutions = {
        "$$FLAGS$$": ", ".join(['"{}"'.format(f) for f in ctx.attr.args]).strip(),
        # Leaving CHDIR empty results in potentially user facing issues w/
        # black and flake8, so we'll just assign something trivial as a no-op.
        "$$CHDIR$$": "os.chdir('{}')".format(ctx.attr.chdir) if ctx.attr.chdir else "_ = 0",
    }

    ctx.actions.expand_template(
        template = ctx.file.template,
        output = ctx.outputs.out,
        substitutions = dict(substitutions, **ctx.var),
        is_executable = False,
    )

_py_pytest_main = rule(
    implementation = _py_pytest_main_impl,
    attrs = {
        "args": attr.string_list(
            doc = "Additional arguments to pass to pytest.",
        ),
        "chdir": attr.string(
            doc = "A path to a directory to chdir when the test starts.",
            mandatory = False,
        ),
        "out": attr.output(
            doc = "The output file.",
            mandatory = True,
        ),
        "template": attr.label(
            allow_single_file = True,
            default = Label("//rules/private:pytest.py.tmpl"),
        ),
    },
)

def py_pytest_main(name, py_library = _py_library, **kwargs):
    """py_pytest_main wraps the template rendering target and the final py_library.

    Args:
        name: The name of the runable target that updates the test entry file.
        py_library: Use this attribute to override the default py_library rule.
        **kwargs: The extra arguments passed to the template rendering target.
    """

    test_main = name + ".py"
    tags = kwargs.pop("tags", [])
    visibility = kwargs.pop("visibility", [])

    _py_pytest_main(
        name = "%s_template" % name,
        out = test_main,
        tags = tags,
        visibility = visibility,
        **kwargs
    )

    py_library(
        name = name,
        srcs = [test_main],
        tags = tags,
        visibility = visibility,
    )
