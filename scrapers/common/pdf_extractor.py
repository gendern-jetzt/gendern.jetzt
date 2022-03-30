import os
import fitz
from common.nextcloud import NextCloud
from more_itertools import islice_extended

import config


class PdfExtractor:
    def __init__(self, dir):
        self.nc = NextCloud(
            config.nextcloud_url,
            config.nxc_credentials["username"],
            config.nxc_credentials["password"],
        )
        self.dir = dir

    def _iter_pages(self, data):
        with fitz.open(stream=data, filetype="pdf") as doc:
            for page in doc:
                yield page.get_text()

    def iter_pipeline_files(self, source, skip_first_n_pages, skip_last_n_pages):
        file_paths = self.nc.list_dir(self.dir)
        remove_non_pdf = [
            filename for filename in file_paths if filename.endswith("pdf")
        ]
        for text_url in remove_non_pdf:
            base = os.path.basename(text_url)
            issue_id = os.path.splitext(base)[0]
            issue = []
            data = self.nc.get_file(text_url)
            pages = self._iter_pages(data)
            pages = islice_extended(pages, skip_first_n_pages, -skip_last_n_pages)
            for id_page, page in enumerate(pages):
                if page:
                    issue.append(
                        {
                            "source": source,
                            "source_id": "/".join((issue_id, str(id_page))),
                            "cleaned_text": page,
                            "raw_data": page,
                        }
                    )
            yield issue
        yield []
