from pathlib import Path

import click
import requests
from config import PIPELINE_URL


@click.command()
@click.argument("CORPUS_FOLDER", type=Path)
def main(corpus_folder):
    corpus_folder.mkdir(exist_ok=True)
    corpus_data = requests.get(f"{PIPELINE_URL}/export_corpus")
    assert corpus_data.ok
    with open(corpus_folder / "corpus.json", "w") as f:
        f.write(corpus_data.text)


if __name__ == "__main__":
    main()
