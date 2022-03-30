from common.pdf_extractor import PdfExtractor
from common.pipeline import Pipeline

import config

pdf_extractor = PdfExtractor(dir="uploads/iz3w")
pipeline = Pipeline(config.PIPELINE_URL)

for id, issue in enumerate(
    pdf_extractor.iter_pipeline_files(
        source="iz3w", skip_first_n_pages=5, skip_last_n_pages=5
    )
):
    pipeline.add_texts(issue)
    print("Issue", id, end="\r")
