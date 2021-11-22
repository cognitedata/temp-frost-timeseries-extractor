from dataclasses import dataclass

from cognite.extractorutils.configtools import BaseConfig, StateStoreConfig


@dataclass
class FrostEndpoints:
    locations: str
    sources: str
    available_timeseries: str
    observations: str


@dataclass
class FrostConfig:
    client_id: str
    endpoints: FrostEndpoints


@dataclass
class TimeSeriesConfig:
    id: int
    sensory_system_id: str
    variable: str
    time_res: str
    valid_from: str


@dataclass
class ExtractorConfig:
    state_store: StateStoreConfig = StateStoreConfig()


@dataclass
class Config(BaseConfig):
    frost_cfg: FrostConfig
    timeseries_cfg: TimeSeriesConfig
    extractor: ExtractorConfig = ExtractorConfig()
