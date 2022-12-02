workspace(name = "com_github_bentoml_plugins")

load("//rules:deps.bzl", "internal_deps")

internal_deps()

load("@com_github_bentoml_bentoml//rules:deps.bzl", "bentoml_dependencies")

bentoml_dependencies()

load("@com_github_bentoml_bentoml//rules:workspace0.bzl", "workspace0")

workspace0()

load("@com_github_bentoml_bentoml//rules:workspace1.bzl", "workspace1")

workspace1()

load("@com_github_bentoml_bentoml//rules:workspace2.bzl", "workspace2")

workspace2()

load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "plugins",
    requirements_lock = "//requirements:dev-requirements.lock.txt",
)

load("@plugins//:requirements.bzl", "install_deps")

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
