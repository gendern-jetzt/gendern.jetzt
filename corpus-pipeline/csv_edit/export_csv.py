import argparse
import datetime
import json
import os
import sys

import pandas as pd
import requests


def export_csv(max, URL, name=None):
    if name is None:
        time_stamp = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        name = time_stamp + "_csv_export.csv"
    if os.path.exists(name):
        print("path {} already exists!".format(name))
        sys.exit(1)

    reply = requests.get(f"{URL}?max={max}")
    print(reply.text)
    if reply.status_code != 200:
        print(
            "Server returned {} as status code of response!".format(reply.status_code)
        )
        sys.exit(1)

    reply_json = json.loads(reply.text)
    if len(reply_json) == 0:
        print("No data received from server.")
        sys.exit(2)
    df = pd.DataFrame(x for x in reply_json)
    df.insert(3, "manually_ungendered", df["sentence_ungendered"])

    df.to_csv(name, index=False, sep=";")
    print(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max", help="max number of sentences to export from database", default=100
    )
    parser.add_argument("--name", help="file name of csv e.g myFile.csv", default=None)
    parser.add_argument(
        "--url", help="URL from which the data is exported", required=True
    )
    args = parser.parse_args()
    export_csv(max=args.max, name=args.name, URL=args.url)
