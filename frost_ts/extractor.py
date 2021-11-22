import logging
from threading import Event

from cognite.client import CogniteClient
from cognite.extractorutils.statestore import AbstractStateStore

from frost_ts.config import Config
from frost_ts.utils import get_timeseries

logger = logging.getLogger(__name__)


def run_extractor(cognite: CogniteClient, states: AbstractStateStore, config: Config, stop_event: Event) -> None:
    datapoints, stop_date = get_timeseries(config.frost_cfg, config.timeseries_cfg, logger)
    logger.info(f"Injecting total of <{len(datapoints)}> data points to timeserie <{config.timeseries_cfg.id}>!")
    cognite.datapoints.insert(datapoints, id=config.timeseries_cfg.id)
    file_obj = open("last.extraction", "w")
    file_obj.write(stop_date)
    file_obj.close()
