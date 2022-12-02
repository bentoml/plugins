load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

def internal_deps():
    maybe(
        git_repository,
        name = "com_github_bentoml_bentoml",
        remote = "https://github.com/aarnphm/bentoml.git",
        branch = "fix/tools",
    )

    maybe(
        git_repository,
        name = "io_tweag_rules_nixpkgs",
        remote = "https://github.com/tweag/rules_nixpkgs.git",
        commit = "d91ee74ae365dd1f74261e4fa04ff4dbc48cd323",
        shallow_since = "1669908476 +0000",
    )
