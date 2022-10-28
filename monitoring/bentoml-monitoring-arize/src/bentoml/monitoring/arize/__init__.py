from __future__ import annotations

import os
import typing as t
import logging
import datetime
import collections

import attr
from arize.api import Client  # type: ignore
from arize.api import Embedding  # type: ignore
from arize.api import ModelTypes  # type: ignore
from arize.utils.types import Environments  # type: ignore

from bentoml.monitoring import MonitorBase

BENTOML_MONITOR_ROLES = {"feature", "prediction", "actual"}
BENTOML_MONITOR_TYPES = {"numerical", "categorical", "numerical_sequence"}
logger = logging.getLogger(__name__)
DataType: t.TypeAlias = str | int | float | bool


@attr.define(auto_attribs=True)
class ArizeForm:
    prediction_label_column: str | None = None
    prediction_score_column: str | None = None
    actual_label_column: str | None = None
    actual_score_column: str | None = None
    feature_columns: list[str] | None = None
    embedding_feature_columns: list[str] | None = None


class ArizeMonitor(MonitorBase[DataType]):
    """ """

    PRESERVED_COLUMNS = (COLUMN_TIME, COLUMN_RID) = ("timestamp", "request_id")

    def __init__(
        self,
        name: str,
        api_key: str | None = None,
        space_key: str | None = None,
        uri: str = "https://api.arize.com/v1",
        max_workers: int = 1,
        max_queue_bound: int = 5000,
        timeout: int = 200,
        model_type: ModelTypes | None = None,
        model_id: str | None = None,
        model_version: str | None = None,
        model_environment: Environments | None = None,
        model_tags: t.Dict[str, str] | None = None,
    ):
        self.name = name

        # client options
        if api_key is None:
            api_key = os.environ.get("ARIZE_API_KEY")
        assert api_key is not None, "api_key is required"
        self.api_key = api_key
        if space_key is None:
            space_key = os.environ.get("ARIZE_SPACE_KEY")
        assert space_key is not None, "space_key is required"
        self.space_key = space_key
        self.uri = uri
        self.max_workers = max_workers
        self.max_queue_bound = max_queue_bound
        self.timeout = timeout

        # model options
        self.model_type = model_type
        self.model_id = model_id
        self.model_version = model_version
        self.model_environment = model_environment
        self.model_tags = model_tags

        self._form = ArizeForm()

        # internal state
        self._is_first_record = True
        self._is_first_column = False
        self._schema: list[dict[str, str]] = []
        self._arize_schema: list[dict[str, str]] = []
        self._columns: dict[
            str,
            collections.deque[DataType],
        ] = collections.defaultdict(collections.deque)

    def _init_client(self):
        self._client = Client(
            api_key=self.api_key,
            space_key=self.space_key,
            uri=self.uri,
            max_workers=self.max_workers,
            max_queue_bound=self.max_queue_bound,
            timeout=self.timeout,
        )

    def _infer_model_type(self):
        """
        https://docs.arize.com/arize/model-schema-mapping#performance-metrics
        """
        assert self._schema
        numeric_flag = 0
        categorical_flag = 0
        for column in self._schema:
            if column["type"] == "categorical" and column["role"] == "prediction":
                categorical_flag += 1
            elif column["type"] == "numerical" and column["role"] == "prediction":
                numeric_flag += 1
        if categorical_flag == 1 and numeric_flag >= 1:
            return ModelTypes.SCORE_CATEGORICAL
        if categorical_flag == 1 and numeric_flag == 0:
            return ModelTypes.SCORE_CATEGORICAL
        if numeric_flag:
            return ModelTypes.NUMERIC
        raise ValueError("Cannot infer model type from schema")

    def start_record(self) -> None:
        """
        Start recording data. This method should be called before logging any data.
        """
        self._is_first_column = True

    def stop_record(self) -> None:
        """
        Stop recording data. This method should be called after logging all data.
        """
        if self._is_first_record:
            self.export_schema()
            self._is_first_record = False

        if self._is_first_column:
            logger.warning("No data logged in this record. Will skip this record.")
        else:
            self.export_data()

    def export_schema(self):
        """
        Export schema of the data. This method should be called after all data is logged.
        """
        if self.model_type is None:
            self.model_type = self._infer_model_type()
        if self.model_version is None and self.model_id is None:
            from bentoml._internal.context import component_context

            self.model_id = component_context.bento_name
            self.model_version = component_context.bento_version
        if self.model_environment is None:
            self.model_environment = Environments.PRODUCTION

    def _yield_arize_data(self):
        pass

    def export_data(self):
        """
        Export data. This method should be called after all data is logged.
        """
        assert (
            len(set(len(q) for q in self._columns.values())) == 1
        ), "All columns must have the same length"
        while True:
            try:
                record = {k: v.popleft() for k, v in self._columns.items()}
                self._client.log(
                    model_id=self.model_id,
                    model_type=self.model_type,
                    environment=self.model_environment,
                    model_version=self.model_version,
                    tags=self.model_tags,
                    prediction_id=record[self.COLUMN_RID],
                    prediction_timestamp=record[self.COLUMN_TIME],
                    batch_id=None,
                    prediction_label: Union[str, bool, int, float, Tuple[str, float]] = None,
                    actual_label: Union[str, bool, int, float, Tuple[str, float]] = None,
                    features: Optional[Dict[str, Union[str, bool, float, int]]] = None,
                    embedding_features: Optional[Dict[str, Embedding]] = None,
                    shap_values: Dict[str, float] = None,
                )
            except IndexError:
                break

    def log(
        self,
        data: DataType,
        name: str,
        role: str,
        data_type: str,
    ) -> None:
        """
        log a data with column name, role and type to the current record
        """
        if name in self.PRESERVED_COLUMNS:
            raise ValueError(
                f"Column name {name} is preserved. Please use a different name."
            )

        assert role in BENTOML_MONITOR_ROLES, f"Invalid role {role}"
        assert data_type in BENTOML_MONITOR_TYPES, f"Invalid data type {data_type}"

        if self._is_first_record:
            self._schema.append({"name": name, "role": role, "type": data_type})
        if self._is_first_column:
            self._is_first_column = False

            from bentoml._internal.context import trace_context

            # universal columns
            self._columns[self.COLUMN_TIME].append(datetime.datetime.now().timestamp())
            assert trace_context.request_id is not None
            self._columns[self.COLUMN_RID].append(trace_context.request_id)

        self._columns[name].append(data)

    def log_batch(
        self,
        data_batch: t.Iterable[DataType],
        name: str,
        role: str,
        data_type: str,
    ) -> None:
        """
        Log a batch of data. The data will be logged as a single column.
        """
        try:
            for data in data_batch:
                self.log(data, name, role, data_type)
        except TypeError:
            raise ValueError(
                "data_batch is not iterable. Please use log() to log a single data."
            ) from None

    def log_table(
        self,
        data: t.Iterable[t.Iterable[DataType]],
        schema: dict[str, str],
    ) -> None:
        raise NotImplementedError("Not implemented yet")
