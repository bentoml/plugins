import concurrent.futures as cf
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Union
from typing import Optional

from arize.utils.types import Embedding
from arize.utils.types import ModelTypes
from arize.utils.types import Environments

class Client:
    """
    Arize API Client to log model predictions and actuals to the Arize AI platform
    """

    def __init__(
        self,
        api_key: str,
        space_key: str,
        uri: Optional[str] = ...,
        max_workers: Optional[int] = ...,
        max_queue_bound: Optional[int] = ...,
        timeout: Optional[int] = ...,
    ) -> None:
        """
        :param api_key (str): api key associated with your account with Arize AI.
        :param space_key (str): space key in Arize AI.
        :param uri (str, optional): uri to send your records to Arize AI. Defaults to "https://api.arize.com/v1".
        :param max_workers (int, optional): number of max concurrent requests to Arize. Defaults to 8.
        :param max_queue_bound (int, optional): number of maximum concurrent future objects being generated for publishing to Arize. Defaults to 5000.
        :param timeout (int, optional): How long to wait for the server to send data before giving up. Defaults to 200.
        """
        ...
    def log(
        self,
        prediction_id: Union[str, int, float],
        model_id: str,
        model_type: ModelTypes,
        environment: Environments,
        model_version: Optional[str] = ...,
        prediction_timestamp: Optional[int] = ...,
        prediction_label: Union[str, bool, int, float, Tuple[str, float], None] = ...,
        actual_label: Union[str, bool, int, float, Tuple[str, float], None] = ...,
        features: Optional[Dict[str, Union[str, bool, float, int]]] = ...,
        embedding_features: Optional[Dict[str, Embedding]] = ...,
        shap_values: Dict[str, float] = ...,
        tags: Optional[Dict[str, Union[str, bool, float, int]]] = ...,
        batch_id: Optional[str] = ...,
    ) -> cf.Future[Any]:
        """Logs a record to Arize via a POST request.
        :param prediction_id (str, int, or float): Unique string identifier for a specific prediction. This value is used to match a prediction to an actual label or feature imporances in the Arize platform.
        :param model_id (str): Unique identifier for a given model
        :param model_type (ModelTypes): Declares what model type this prediction is for. Must be one of: Numeric, Score_Categorical.
        :param environment (Environments): The environment that this dataframe is for (Production, Training, Validation).
        :param model_version (str, optional): Field used to group together a subset of predictions and actuals for a given model_id. Defaults to None.
        :param prediction_timestamp (int, optional): Unix epoch time in seconds for prediction. Defaults to None.
                    If None, prediction uses current timestamp.
        :param prediction_label (bool, int, float, str, or Tuple(str, float); optional): The predicted value for a given model input. Defaults to None.
        :param actual_label (bool, int, float, str, or Tuple[str, float]; optional): The actual true value for a given model input. This actual will be matched to the prediction with the same prediction_id as the one in this call. Defaults to None.
        :param features (Dict[str, <value>], optional): Dictionary containing human readable and debuggable model features. Keys must be strings.
                    Values must be one of str, bool, float, long. Defaults to None.
        :param embedding_features (Dict[str, Embedding], optional): Dictionary containing model embedding features. Keys must be strings.
                    Values must be of Embedding type. Defaults to None.
        :param shap_values (Dict[str, float], optional): Dictionary containing human readable and debuggable model features keys, along with SHAP feature importance values. Keys must be str, while values must be float. Defaults to None.
        :param tags (Dict[str, <value>], optional): Dictionary containing human readable and debuggable model tags. Keys must be strings.
                    Values must be one of str, bool, float, long. Defaults to None.
        :param batch_id (str, optional): Used to distinguish different batch of data under the same model_id and model_version. Required when environment is VALIDATION. Defaults to None.
        :return: `concurrent.futures.Future` object
        """
        ...
