workspace(name = "com_github_bentoml_ecosystem")

load("//bazel:deps.bzl", "internal_deps")

internal_deps()

load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")

go_rules_dependencies()

go_register_toolchains(version = "1.19")

load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

gazelle_dependencies()

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

python_register_toolchains(
    name = "python310",
    python_version = "3.10",
)

load("@python310//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "ecosystem",
    python_interpreter_target = interpreter,
    requirements_lock = "//requirements:dev-requirements.lock.txt",
)

# We are vendoring dependencies requirements from pip_parse
# This way our Bazel doesn't eagerly fetch and install the pip_parse'd
# repository for builds that don't need it.
load("//:requirements.bzl", "install_deps")

install_deps()

load("@io_tweag_rules_nixpkgs//nixpkgs:repositories.bzl", "rules_nixpkgs_dependencies")

rules_nixpkgs_dependencies()

load("@io_tweag_rules_nixpkgs//nixpkgs:nixpkgs.bzl", "nixpkgs_git_repository", "nixpkgs_package")

# Sync with nix/sources.json
nixpkgs_git_repository(
    name = "nixpkgs",
    revision = "2e193264db568a42b342e4b914dc314383a6194c",
)

# include nixfmt and niv
nixpkgs_package(
    name = "niv",
    attribute_path = "pkgs.niv",
    repository = "@nixpkgs",
)

nixpkgs_package(
    name = "nixfmt",
    attribute_path = "pkgs.nixfmt",
    repository = "@nixpkgs",
)
