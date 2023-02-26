"""
BentoML Monitoring Arize plugin.
=======

BentoML is the unified ML Model Serving framework. Data Scientists and ML Engineers use
BentoML to:

* Accelerate and standardize the process of taking ML models to production across teams
* Build reliable, scalable, and high performance model serving systems
* Provide a flexible MLOps platform that grows with your Data Science needs

To learn more, visit BentoML documentation at: http://docs.bentoml.org
To get involved with the development, find us on GitHub: https://github.com/bentoml
And join us in the BentoML slack community: https://l.linklyhq.com/l/ktOh
"""
from __future__ import annotations

import os
import typing as t
import logging
import datetime
import functools
import collections
from enum import Enum
from enum import unique
from typing import TYPE_CHECKING

import attr
from arize.api import Client
from arize.utils.types import Embedding
from arize.utils.types import ModelTypes
from arize.utils.types import Environments

from bentoml.monitoring import MonitorBase
from bentoml._internal.context import trace_context
from bentoml._internal.context import component_context

BENTOML_MONITOR_ROLES = {"feature", "prediction", "target"}
BENTOML_MONITOR_TYPES = {"numerical", "categorical", "numerical_sequence"}
logger = logging.getLogger(__name__)

# Note that DataType is a runtime type.
DataType = t.Union[str, int, float, bool, t.List[float]]


@unique
class Mapping(Enum):
    """
    Mapping solutions for bentoml data fields to arize data fields
    """

    SCORED_CLASSIFICATION = 1
    CLASSIFICATION = 2
    REGRESSION = 3
    RANKING = 4


@attr.define(auto_attribs=True)
class _FieldStats:
    prediction_label_columns: list[str] = attr.field(factory=list)
    prediction_score_columns: list[str] = attr.field(factory=list)
    actual_label_columns: list[str] = attr.field(factory=list)
    actual_score_columns: list[str] = attr.field(factory=list)
    feature_columns: list[str] = attr.field(factory=list)
    embedding_feature_columns: list[str] = attr.field(factory=list)


def _stat_fields(schema: t.Iterable[dict[str, str]]) -> _FieldStats:
    fields = _FieldStats()
    for column in schema:
        if column["role"] == "feature":
            if column["type"] == "numerical_sequence":
                fields.embedding_feature_columns.append(column["name"])
            else:
                fields.feature_columns.append(column["name"])
        elif column["type"] == "categorical" and column["role"] == "prediction":
            fields.prediction_label_columns.append(column["name"])
        elif column["type"] == "numerical" and column["role"] == "prediction":
            fields.prediction_score_columns.append(column["name"])
        elif column["type"] == "numerical_sequence" and column["role"] == "prediction":
            logger.warning(
                "Arize Monitor does not support numerical_sequence for prediction. "
                "Ignoring column %s",
                column["name"],
            )
        elif column["type"] == "categorical" and column["role"] == "target":
            fields.actual_label_columns.append(column["name"])
        elif column["type"] == "numerical" and column["role"] == "target":
            fields.actual_score_columns.append(column["name"])
        elif column["type"] == "numerical_sequence" and column["role"] == "target":
            logger.warning(
                "Arize Monitor does not support numerical_sequence for target. "
                "Ignoring column %s",
                column["name"],
            )
        else:
            logger.warning(
                "Arize Monitor does not support column %s with role %s and type %s. Ignoring column",
                column["name"],
                column["role"],
                column["type"],
            )
    return fields


def _is_valid_classification_form(fields: _FieldStats, warn: bool = False) -> bool:
    if fields.prediction_label_columns and not fields.prediction_score_columns:
        if warn and len(fields.prediction_label_columns) > 1:
            logger.warning(
                "Arize only supports single prediction label column, column %s will be ignore",
                fields.prediction_label_columns[1:],
            )
        return True
    if fields.actual_label_columns and not fields.actual_score_columns:
        if warn and len(fields.actual_label_columns) > 1:
            logger.warning(
                "Arize only supports single actual label column, column %s will be ignore",
                fields.actual_label_columns[1:],
            )
        return True
    return False


def _is_valid_scored_classification_form(
    fields: _FieldStats, warn: bool = False
) -> bool:
    if fields.prediction_label_columns and fields.prediction_score_columns:
        if warn and len(fields.prediction_label_columns) > 1:
            logger.warning(
                "Arize only supports single prediction label column, column %s will be ignore",
                fields.prediction_label_columns[1:],
            )
        if warn and len(fields.prediction_score_columns) > 1:
            logger.warning(
                "Arize only supports single prediction score column, column %s will be ignore",
                fields.prediction_score_columns[1:],
            )
        return True
    if fields.actual_label_columns and fields.actual_score_columns:
        if warn and len(fields.actual_label_columns) > 1:
            logger.warning(
                "Arize only supports single actual label column, column %s will be ignore",
                fields.actual_label_columns[1:],
            )
        if warn and len(fields.actual_score_columns) > 1:
            logger.warning(
                "Arize only supports single actual score column, column %s will be ignore",
                fields.actual_score_columns[1:],
            )
        return True
    return False


def _is_valid_regression_form(fields: _FieldStats, warn: bool = False) -> bool:
    if fields.prediction_score_columns and not fields.prediction_label_columns:
        if warn and len(fields.prediction_score_columns) > 1:
            logger.warning(
                "Arize only supports single prediction score column, column %s will be ignore",
                fields.prediction_score_columns[1:],
            )
        return True
    if fields.actual_score_columns and not fields.actual_label_columns:
        if warn and len(fields.actual_score_columns) > 1:
            logger.warning(
                "Arize only supports single actual score column, column %s will be ignore",
                fields.actual_score_columns[1:],
            )
        return True
    return False


def _infer_mapping(
    fields: _FieldStats,
    model_type: ModelTypes | None = None,
) -> Mapping:
    """
    Infer the mapping solution for bentoml data fields to arize data fields
    https://docs.arize.com/arize/model-schema-mapping#performance-metrics
    """
    if model_type is None:
        if _is_valid_scored_classification_form(fields):
            mapping = Mapping.SCORED_CLASSIFICATION
        elif _is_valid_classification_form(fields):
            mapping = Mapping.CLASSIFICATION
        elif _is_valid_regression_form(fields):
            mapping = Mapping.REGRESSION
        else:
            raise ValueError(
                "failed to find a valid mapping to arize schema for the given schema. "
                "Please specify a mapping using the `model_type` parameter."
            )
    elif model_type == ModelTypes.SCORE_CATEGORICAL:
        if _is_valid_scored_classification_form(fields, warn=True):
            mapping = Mapping.SCORED_CLASSIFICATION
        elif _is_valid_classification_form(fields, warn=True):
            mapping = Mapping.CLASSIFICATION
        else:
            raise ValueError("Not a valid arize classification schema")
    elif model_type == ModelTypes.NUMERIC:
        if _is_valid_regression_form(fields, warn=True):
            mapping = Mapping.REGRESSION
        else:
            raise ValueError("Not a valid arize regression schema")
    else:
        logger.warning(
            "Arize Monitor does not support model type %s. Falling back to default mapping"
        )
        mapping = Mapping.REGRESSION
    return mapping


_mapping_to_model_type = {
    Mapping.SCORED_CLASSIFICATION: ModelTypes.SCORE_CATEGORICAL,
    Mapping.CLASSIFICATION: ModelTypes.SCORE_CATEGORICAL,
    Mapping.REGRESSION: ModelTypes.NUMERIC,
}


if TYPE_CHECKING:
    MapData: t.TypeAlias = tuple[
        DataType | tuple[DataType, DataType] | None,
        DataType | tuple[DataType, DataType] | None,
        dict[str, DataType],
        dict[str, Embedding],
    ]


def _map_data(
    record: dict[str, DataType], fields: _FieldStats, mapping: Mapping
) -> MapData:
    """
    Map bentoml monitoring record to arize fields
    """
    if mapping == Mapping.SCORED_CLASSIFICATION:
        prediction_label = (
            (
                str(record[fields.prediction_label_columns[0]]),
                record[fields.prediction_score_columns[0]],
            )
            if fields.prediction_label_columns
            else None
        )
        actual_label = (
            (
                record[fields.actual_label_columns[0]],
                record[fields.actual_score_columns[0]],
            )
            if fields.actual_label_columns
            else None
        )
    elif mapping == Mapping.CLASSIFICATION:
        prediction_label = (
            str(record[fields.prediction_label_columns[0]])
            if fields.prediction_label_columns
            else None
        )
        actual_label = (
            record[fields.actual_label_columns[0]]
            if fields.actual_label_columns
            else None
        )
    elif mapping == Mapping.REGRESSION:
        prediction_label = (
            record[
                (fields.prediction_score_columns + fields.prediction_label_columns)[0]
            ]
            if fields.prediction_score_columns or fields.prediction_label_columns
            else None
        )
        actual_label = (
            record[(fields.actual_score_columns + fields.actual_label_columns)[0]]
            if fields.actual_score_columns or fields.actual_label_columns
            else None
        )
    else:
        logger.warning("Mapping not supported. Fallback to regression")
        prediction_label = (
            record[fields.prediction_score_columns[0]]
            if fields.prediction_score_columns
            else None
        )
        actual_label = (
            record[fields.actual_score_columns[0]]
            if fields.actual_score_columns
            else None
        )
    features = {c: record[c] for c in fields.feature_columns}
    embedding_features = {
        c: Embedding(vector=record[c]) for c in fields.embedding_feature_columns  # type: ignore
    }
    return prediction_label, actual_label, features, embedding_features


class ArizeMonitor(MonitorBase[DataType]):
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
        environment: Environments | None = None,
        model_tags: dict[str, str | bool | float | int] | None = None,
        **kwargs: t.Any,
    ):
        super().__init__(name, **kwargs)

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
        self.environment = environment
        self.model_tags = model_tags

        # internal state
        self._is_recording = False
        self._is_first_record = True
        self._is_first_column = False
        self._schema: dict[str, dict[str, str]] = {}
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

    def export_schema(self, columns_schema: dict[str, dict[str, str]]) -> None:
        """
        Export schema of the data. This method should be called right after the first record.
        """
        fields = _stat_fields(columns_schema.values())
        mapping = _infer_mapping(fields, self.model_type)
        self._data_converter = functools.partial(
            _map_data, fields=fields, mapping=mapping
        )

        if self.model_type is None:
            self.model_type = _mapping_to_model_type[mapping]

        if self.model_version is None and self.model_id is None:
            self.model_id = f"{component_context.bento_name}:{self.name}"
            self.model_version = component_context.bento_version

        if self.environment is None:
            self.environment = Environments.PRODUCTION

        self._init_client()

    def export_data(self, datas: dict[str, collections.deque[DataType]]) -> None:
        """
        Export data. This method should be called after all data is logged.
        """
        assert self.model_id is not None
        assert self.model_type is not None
        assert self.environment is not None

        timestamp = datetime.datetime.now().timestamp()
        prediction_id = trace_context.request_id
        assert isinstance(prediction_id, int)
        while True:
            try:
                record = {k: v.popleft() for k, v in datas.items()}
            except IndexError:
                break
            (
                prediction_label,
                actual_label,
                features,
                embedding_features,
            ) = self._data_converter(record)

            self._client.log(
                model_id=self.model_id,
                model_type=self.model_type,
                environment=self.environment,
                model_version=self.model_version,
                tags=self.model_tags,
                prediction_id=prediction_id,
                prediction_timestamp=int(timestamp),
                batch_id=None,
                prediction_label=prediction_label,  # type: ignore (invariant types)
                actual_label=actual_label,  # type: ignore (invariant types)
                features=features,  # type: ignore (invariant types)
                embedding_features=embedding_features,
            )
