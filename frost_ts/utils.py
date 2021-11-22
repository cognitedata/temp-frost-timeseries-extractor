from copy import deepcopy
from datetime import datetime
from logging import Logger
from os.path import exists
from typing import Any, List, Tuple

import requests
from dateutil import parser

from frost_ts.config import FrostConfig, TimeSeriesConfig


def check_request(r: requests.models.Response, success_message: str, logger: Logger) -> Any:
    json = r.json()
    if r.status_code == 200:
        data = json["data"]
        logger.info(success_message)
        return data
    else:
        logger.info(f"Error! Returned status code {r.status_code}")
        logger.info(f"Message: {json['error']['message']}")
        logger.info(f"Reason: {json['error']['reason']}")
        raise Exception(f"Reason: {json['error']['reason']}")


def get_start_date(ts_cfg: TimeSeriesConfig) -> Any:
    if exists("last.extraction"):
        file_obj = open("last.extraction", "r")
        return file_obj.read()
    else:
        return ts_cfg.valid_from


def get_range(ts_cfg: TimeSeriesConfig) -> Tuple[str, str]:
    start_date = get_start_date(ts_cfg)
    stop_date = datetime.utcnow().isoformat()
    return start_date, stop_date


def get_endpoint(frost_cfg: FrostConfig, ts_cfg: TimeSeriesConfig, logger: Logger) -> Tuple[str, str, str]:
    start_date, stop_date = get_range(ts_cfg)
    logger.info(
        f"Iniate fetching timeseries of <{ts_cfg.variable}> with time resolution of <{ts_cfg.time_res}> from sensory system <{ts_cfg.sensory_system_id}>!"
    )
    logger.info(f"Period for which timeseries data points will be fetch are from <{start_date}> until <{stop_date}>!")
    endpoint_cfg = {
        "insert_sn_id": ts_cfg.sensory_system_id,
        "insert_start_date": start_date,
        "insert_stop_date": stop_date,
        "insert_variable": ts_cfg.variable,
        "insert_resolution": ts_cfg.time_res,
    }

    endpoint = deepcopy(frost_cfg.endpoints.observations)

    for key, value in endpoint_cfg.items():
        endpoint = endpoint.replace(key, value)

    return endpoint, start_date, stop_date


def create_datapoints(data: List, logger: Logger) -> List:
    logger.info(f"Wrangling total of <{len(data)}> data points!")
    datapoints = []
    for point in data:
        ref_time = parser.isoparse(point["referenceTime"]).replace(tzinfo=None)
        value = point["observations"][0]["value"]
        datapoints += [(ref_time, value)]
    return datapoints


def get_timeseries(frost_cfg: FrostConfig, ts_cfg: TimeSeriesConfig, logger: Logger) -> Tuple[List[Any], str]:
    endpoint, _, stop_date = get_endpoint(frost_cfg, ts_cfg, logger)
    r = requests.get(endpoint, auth=(frost_cfg.client_id, ""))
    data = check_request(r, "Data points succefully fetched", logger)
    datapoints = create_datapoints(data, logger)

    return datapoints, stop_date
