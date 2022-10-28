from __future__ import annotations

import typing as t

import pytest
import arize.api

# from arize.api import Client
from arize.utils.types import ModelTypes


class Client:
    LOG_ARGS = []
    INIT_ARGS = []

    def __init__(
        self,
        api_key: str,
        space_key: str,
        uri: t.Optional[str] = "https://api.arize.com/v1",
        max_workers: t.Optional[int] = 8,
        max_queue_bound: t.Optional[int] = 5000,
        timeout: t.Optional[int] = 200,
    ):
        self.INIT_ARGS.append(locals())

    def log(
        self,
        prediction_id: t.Union[str, int, float],
        model_id: str,
        model_type,
        environment,
        model_version=None,
        prediction_timestamp=None,
        prediction_label=None,
        actual_label=None,
        features=None,
        embedding_features=None,
        shap_values=None,
        tags=None,
        batch_id=None,
    ):
        self.LOG_ARGS.append(locals())


MY_SPACE_KEY = "my_space_key"
MY_API_KEY = "my_api_key"
URI = "http://localhost:5000/v1"
BENTO_NAME = "my_bento_name"
BENTO_VERSION = "my_bento_version"
REQUEST_ID = 214121


@pytest.fixture(autouse=True)
def init_context(monkeypatch):
    from bentoml._internal.context import trace_context
    from bentoml._internal.context import component_context

    trace_context.request_id = REQUEST_ID
    component_context.bento_name = BENTO_NAME
    component_context.bento_version = BENTO_VERSION

    monkeypatch.setattr(arize.api, "Client", Client)


def test_mapping(init_context) -> None:
    from bentoml_monitoring_arize import ArizeMonitor

    monitor = ArizeMonitor(
        "my_monitor_1",
        space_key=MY_SPACE_KEY,
        api_key=MY_API_KEY,
        uri=URI,
    )
    monitor.start_record()
    monitor.log(1, name="pred", role="prediction", data_type="categorical")
    monitor.stop_record()
    assert monitor.model_type == ModelTypes.SCORE_CATEGORICAL
    assert Client.INIT_ARGS[-1]["space_key"] == MY_SPACE_KEY
    assert Client.LOG_ARGS[-1]["model_id"] == BENTO_NAME
    assert Client.LOG_ARGS[-1]["model_version"] == BENTO_VERSION
    assert Client.LOG_ARGS[-1]["prediction_id"] == REQUEST_ID
    assert Client.LOG_ARGS[-1]["model_type"] == ModelTypes.SCORE_CATEGORICAL

    monitor = ArizeMonitor(
        "my_monitor_1",
        space_key="my_space_key",
        api_key="my_api_key",
        uri="http://localhost:5000/v1",
    )
    monitor.start_record()
    monitor.log(1, name="pred", role="prediction", data_type="categorical")
    monitor.log(1, name="pred2", role="prediction", data_type="categorical")
    monitor.stop_record()
    assert monitor.model_type == ModelTypes.SCORE_CATEGORICAL

    monitor = ArizeMonitor(
        "my_monitor_2",
        space_key="my_space_key",
        api_key="my_api_key",
        uri="http://localhost:5000/v1",
    )
    monitor.start_record()
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
    monitor.log(1, name="pred", role="prediction", data_type="numerical")
    monitor.log(1, name="pred2", role="prediction", data_type="numerical")
    monitor.stop_record()
    assert monitor.model_type == ModelTypes.NUMERIC
