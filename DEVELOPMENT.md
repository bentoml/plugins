Install [nix](https://nixos.org/download.html#nix-install-linux) to setup adhoc development environment.

Start new shell:

```bash
nix-shell
```

`ecosystem` vendored python requirements for bazel. See
https://github.com/bazelbuild/rules_python/issues/608 and [this article](https://blog.aspect.dev/avoid-eager-fetches)

We will only vendor requirements from [base-requirements.in](./requirements/base-requirements.in).

To update the vendored requirements rules, do:

```bash
bazel run //:vendor-requirements
```

To update requirements for any `*-requirements.in` changes, do:

```bash
bazel run //:<file>-requirements.update
```
