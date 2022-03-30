import argparse
import itertools
import sys

import pandas as pd
import requests

from tokenizer import tokenizer


def import_csv(file, URL):
    df = pd.read_csv(file, sep=";")
    for index, row in df.iterrows():
        manually_ungendered = list(
            itertools.chain.from_iterable(tokenizer(str(row["manually_ungendered"])))
        )
        ungendered = list(
            itertools.chain.from_iterable(tokenizer(str(row["sentence_ungendered"])))
        )

        indices = []
        for idx, (gendered_word, ungendered_word) in enumerate(
            zip(manually_ungendered, ungendered)
        ):
            if gendered_word != ungendered_word:
                indices.append(idx)

        for idx, i in enumerate(range(1, len(indices) + 1)):
            manually_ungendered.insert(i + indices[idx], "<GENDERLY>")

        indices = []
        for idx, word in enumerate(manually_ungendered[:-1]):
            if word == manually_ungendered[idx + 1] and word == "<GENDERLY>":
                indices.append(idx)

        for idx in sorted(indices, reverse=True):
            del manually_ungendered[idx]

        df.at[index, "manually_ungendered"] = " ".join(manually_ungendered)

    res = requests.post(URL, json=df.to_json(orient="records"))
    if res.ok:
        print("Success!")
    else:
        print("Error: Bad response from server: \n{}".format(res.reason))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="name of file to import to db", required=True)
    parser.add_argument(
        "--url", help="URL to which the data is imported", required=True
    )
    args = parser.parse_args()
    import_csv(file=args.file, URL=args.url)
