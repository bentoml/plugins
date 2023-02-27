{ sources ? import ./nix/sources.nix, pkgs ? import sources.nixpkgs {
  overlays = [ ];
  config = { };
} }:

with pkgs;
let
  lib = import <nixpkgs/lib>;
  inherit (lib) optional optionals;

  packages = with pkgs;
    [
      (python310.withPackages (ps: with ps; [ pynvim pip virtualenv ipython ]))

      # Tooling
      git
      bazel_6
      nixfmt
      treefmt
      zsh

      # Without this, we see a whole bunch of warnings about LANG, LC_ALL and locales in general.
      # The solution is from: https://github.com/NixOS/nix/issues/318#issuecomment-52986702
      glibcLocales
      coreutils
    ] ++ lib.optional stdenv.isLinux inotify-tools
    ++ lib.optionals stdenv.isDarwin
    (with darwin.apple_sdk.frameworks; [ CoreFoundation CoreServices ]);

  env = buildEnv {
    name = "dev-environment";
    paths = packages;
  };

in stdenv.mkDerivation rec {
  name = "ecosystem-environment";

  buildInputs = [ env ];

  shellHook = ''
    if [[ ! -d venv ]]; then
      python -m virtualenv venv --download
      source venv/bin/activate
    else
      source venv/bin/activate
    fi

    ./hack/update-deps
    pip install -r ./requirements/bazel-pypi.lock.txt -r ./requirements/bazel-external.lock.txt
  '';

  # NOTE: Using bazel from nix, which disable the wrapper script
  DISABLE_BAZEL_WRAPPER = true;
  LOCALE_ARCHIVE =
    if stdenv.isLinux then "${glibcLocales}/lib/locale/locale-archive" else "";
}
