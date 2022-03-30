import json

import bs4
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class WordpressScraper:
    def __init__(self, base_url, is_api_url):
        if is_api_url:
            self.base_url = base_url
        else:
            self.base_url = f"{base_url}/wp-json"

        self._session = requests.Session()

        retries = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
        )

        self._session.mount("https://", HTTPAdapter(max_retries=retries))

    def _iter_pages(self, per_page):
        url = f"{self.base_url}/wp/v2/posts/"
        params = {"per_page": per_page}
        while True:
            req = self._session.get(
                url,
                params=params,
                headers={
                    "User-Agent": "Genderly Corpus Scraper (Reach us at kontakt@genderly.eu)"
                },
            )
            yield req.json()
            if "next" in req.links:
                url = req.links["next"]["url"]
            else:
                break

    def iter_posts(self, per_page=100):
        for page in self._iter_pages(per_page):
            for post in page:
                yield post

    def iter_pipeline_batches(self, source_name, per_page=100):
        for page in self._iter_pages(per_page=per_page):
            batch = []
            for post in page:
                post_text = bs4.BeautifulSoup(
                    post["content"]["rendered"], features="html.parser"
                ).text
                batch.append(
                    {
                        "source": source_name,
                        "source_id": str(post["id"]),
                        "cleaned_text": post_text,
                        "raw_data": json.dumps(post),
                    }
                )

            yield batch
        yield []

    def scrape_all_to_pipeline(self, pipeline, **kwargs):
        for batch in self.iter_pipeline_batches(**kwargs):
            pipeline.add_texts(batch)
