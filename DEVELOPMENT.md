# Quickstart

Create a virtualenv for development:

```bash
python -m venv venv
./venv/bin/activate
```

Install development requirements:

```bash
pip install -r requirements/dev-requirements.lock.txt
```

# Using `bazel`

_NOTE: You don't have to use `bazel` and nix to start developing._

`bentoml/plugins` vendored python requirements using bazel and nix. See
https://github.com/bazelbuild/rules_python/issues/608 and [this article](https://blog.aspect.dev/avoid-eager-fetches)

To update the vendor-ed requirements rules, do:

```bash
bazel run //:vendor_requirements
```

To generate a new project run:

```bash
bazel run //tools:bootstrap -- bentoml-monitoring-handler --parent-dir monitoring
```

To see bootstrap flags use:

```bash
bazel run //tools:bootstrap -- --help
```

To run a test:

```bash
bazel test //path/to/project/tests:package.native
```

Get all test queries:

```bash
bazel query 'kind(py_test, tests(//...))'
```

To run formatter:

```bash
bazel run //:format
```

To run lint:

```bash
bazel run //:check
```
