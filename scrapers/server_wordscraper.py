import io

import config
from common.nextcloud import NextCloud
from common.pipeline import Pipeline
from common.wordscraper.wordscraper import word_scrape

pipeline = Pipeline(config.PIPELINE_URL)
nc = NextCloud(
    config.nextcloud_url,
    config.nxc_credentials["username"],
    config.nxc_credentials["password"],
)

file_paths = nc.list_dir("uploads/docx-files")
source = "docx-files"

for id, text_url in enumerate(file_paths[1:]):
    data = nc.get_file(text_url)
    content = word_scrape(io.BytesIO(data))
    texts = [
        {
            "source": text_url.split("/")[-1].split("_")[0],
            "source_id": text_url.split("/")[-1].split("_")[1],
            "cleaned_text": content,
            "raw_data": content,
        }
    ]
    print(texts)
    pipeline.add_texts(texts)
    print(id, "/", len(file_paths), end="\r")
