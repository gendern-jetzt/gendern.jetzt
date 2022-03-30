import json
import random
from itertools import zip_longest
from pathlib import Path

import click


@click.command()
@click.argument("CORPUS_FOLDER", type=Path)
@click.option("--seed", type=int)
@click.option("--test-percentage", type=int, default=10)
@click.option("--dev-percentage", type=int, default=10)
@click.option("--gender-tag", default="GENDER")
@click.option("--no-gender-tag", default="")
def main(
    corpus_folder, seed, test_percentage, dev_percentage, gender_tag, no_gender_tag
):
    corpus_folder.mkdir(exist_ok=True)
    with open(corpus_folder / "corpus.json") as f:
        data = json.load(f)

    if seed is not None:
        random.seed(seed)

    files = {}
    for i in ["test", "dev", "train"]:
        filename = corpus_folder / f"{i}.txt"
        files[i] = open(filename, "w")

    def get_file():
        random_file = random.choices(
            ["test", "dev", "train"],
            weights=[
                test_percentage / 100,
                dev_percentage / 100,
                (100 - test_percentage - dev_percentage) / 100,
            ],
        )[0]
        return files[random_file]

    for sentence in data:
        file = get_file()
        tokens = sentence.split()
        for token, next_token in zip_longest(tokens, tokens[1:]):
            if token == "<GENDERLY>":
                continue
            tag = no_gender_tag
            if next_token == "<GENDERLY>":
                tag = gender_tag
            file.write(f"{token} {tag}\n")
        if tokens:  # Do not add a newline if this sentence had no tokens
            file.write("\n")


if __name__ == "__main__":
    main()
