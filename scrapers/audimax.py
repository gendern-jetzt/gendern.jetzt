from common.nextcloud import NextCloud
from common.pipeline import Pipeline

import config

pipeline = Pipeline(config.PIPELINE_URL)
nc = NextCloud(
    config.nextcloud_url,
    config.nxc_credentials["username"],
    config.nxc_credentials["password"],
)
file_paths = nc.list_dir("uploads/audimax")
source = "audimax"
for id, text_url in enumerate(file_paths[2:]):
    data = nc.get_file(text_url).decode("utf-8")
    texts = [
        {
            "source": source,
            "source_id": str(id),
            "cleaned_text": data,
            "raw_data": data,
        }
    ]
    pipeline.add_texts(texts)
    print(id, "/", len(file_paths), end="\r")
