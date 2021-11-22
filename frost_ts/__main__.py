from cognite.extractorutils import Extractor

from frost_ts import __version__
from frost_ts.config import Config
from frost_ts.extractor import run_extractor


def main() -> None:
    with Extractor(
        name="frost_ts",
        description="Extractor for Frost timesersies for specific location.",
        config_class=Config,
        run_handle=run_extractor,
        version=__version__,
    ) as extractor:
        extractor.run()


if __name__ == "__main__":
    main()
