import argparse
import traceback
import warnings

from common.pipeline import Pipeline
from common.wordpress_scraper import WordpressScraper

from config import PIPELINE_URL

SCRAPERS = {
    # "zett": {"base_url": "https://ze.tt"}, # Zett went offline
    "clickit": {"base_url": "https://www.clickit-magazin.de"},
    "furios": {"base_url": "https://furios-campus.de"},
    "skug": {"base_url": "https://skug.at"},
    "zs-online": {"base_url": "https://zs-online.ch"},
    "cilip": {"base_url": "https://www.cilip.de", "per_page": 10},
    "campusrauschen": {"base_url": "https://campusrauschen.de"},
    "graswurzel": {"base_url": "https://www.graswurzel.net/gwr", "per_page": 10},
    "lateinamerika-nachrichten": {"base_url": "https://lateinamerika-nachrichten.de"},
    "lautschrift": {"base_url": "https://www.lautschrift.org"},
    "kulturundgeschlecht": {
        "base_url": "https://kulturundgeschlecht.blogs.ruhr-uni-bochum.de/index.php?rest_route=",
        "is_api_url": True,
    },
    "ottfried": {"base_url": "https://ottfried.de", "per_page": 10},
    "ruprecht": {"base_url": "https://www.ruprecht.de"},
    "gruene-jugend": {"base_url": "https://gruene-jugend.de"},
}

parser = argparse.ArgumentParser()
parser.add_argument("--limit", action="append", default=[])
args = parser.parse_args()

for limit in args.limit:
    if limit not in SCRAPERS:
        warnings.warn(
            f"'{limit}' was specified as a filter, but no scrapers matches this",
            UserWarning,
        )


pipeline = Pipeline(PIPELINE_URL)
for source_name, kwargs in SCRAPERS.items():
    if args.limit and source_name not in args.limit:
        continue
    print("Scraping", source_name)
    try:
        scraper = WordpressScraper(
            kwargs.pop("base_url"), kwargs.pop("is_api_url", False)
        )
        scraper.scrape_all_to_pipeline(pipeline, source_name=source_name, **kwargs)
    except:  # noqa: E722
        exc_string = traceback.format_exc()
        print(f"Error while scraping {source_name}:")
        print(exc_string)
