load("@bazel_skylib//rules:write_file.bzl", "write_file")

def run_shell(name, srcs = [], content = [], data = [], **kwargs):
    """
    Create a run_shell macro.
    We will create a shell wrapper, and then return a target
    that can be used to run the shell wrapper. The shell wrapper
    will run under $BUILD_WORKSPACE_DIRECTORY.

    Args:
        name: Name of the rule set.
        srcs: List of source files to be used by the rules.
        content: List of rules to be applied.
        data: List of data files to be used by the rules.
        **kwargs: Arbitrary keyword arguments.
    """
    file_name = "_{}_wrapper".format(name)
    shell_file = "{}.sh".format(file_name)

    write_file(
        name = file_name,
        out = shell_file,
        content = [
            "#!/usr/bin/env bash",
            "cd $BUILD_WORKSPACE_DIRECTORY\n",
        ] + content,
    )
    native.sh_binary(
        name = name,
        srcs = [shell_file] + srcs,
        data = data,
        **kwargs
    )
