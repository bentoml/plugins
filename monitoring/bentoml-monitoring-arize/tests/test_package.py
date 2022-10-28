from __future__ import annotations

import typing as t

import pytest
from arize.utils.types import ModelTypes
from bentoml_monitoring_arize import ArizeMonitor


@pytest.fixture
def init_context():
    from bentoml._internal.context import trace_context
    from bentoml._internal.context import component_context

    trace_context.request_id = 1
    component_context.bento_name = "my_bento"
    component_context.bento_version = "asd8casd"


def test_mapping(init_context) -> None:
    monitor = ArizeMonitor(
        "my_monitor_1",
        space_key="my_space_key",
        api_key="my_api_key",
        uri="http://localhost:5000/v1",
    )

    monitor.start_record()
    monitor.log(1, name="foo", role="feature", data_type="numerical")
    monitor.log("assd", name="bar", role="feature", data_type="numerical")
    monitor.log(1, name="pred", role="prediction", data_type="categorical")
    monitor.stop_record()

    assert monitor.model_type == ModelTypes.SCORE_CATEGORICAL

    monitor = ArizeMonitor(
        "my_monitor_2",
        space_key="my_space_key",
        api_key="my_api_key",
        uri="http://localhost:5000/v1",
    )

    monitor.start_record()
    monitor.log(1, name="foo", role="feature", data_type="numerical")
    monitor.log("assd", name="bar", role="feature", data_type="numerical")
    monitor.log(1, name="pred", role="prediction", data_type="numerical")
    monitor.stop_record()

    assert monitor.model_type == ModelTypes.NUMERIC

    monitor = ArizeMonitor(
        "my_monitor_2",
        space_key="my_space_key",
        api_key="my_api_key",
        uri="http://localhost:5000/v1",
    )

    monitor.start_record()
    monitor.log(1, name="foo", role="feature", data_type="numerical")
    monitor.log("assd", name="bar", role="feature", data_type="numerical")
    monitor.log(1, name="pred", role="prediction", data_type="numerical")
    monitor.log(1, name="pred2", role="prediction", data_type="numerical")
    monitor.stop_record()

    assert monitor.model_type == ModelTypes.NUMERIC
