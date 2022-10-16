# ecosystem

_the swish knife to all things bentoml_

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

Get all test query:

```bash
bazel query 'kind(py_test, tests(//...))'
```
