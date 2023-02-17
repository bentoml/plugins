# Quickstart

Create a virtualenv for development:

```bash
python -m venv venv
./venv/bin/activate
```

Install development requirements:

```bash
./hack/update-deps
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
./hack/format
```

To run lint:

```bash
./hack/lint
```
