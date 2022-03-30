# flake8: noqa
# Regex-Based auto degendering

import argparse
import re

SYM = "\/-?|_|\*|:"  # ToDo: sym in array
MARKER = "<GENDERLY>"  # *Genderly


def auto_deg_re(lines):
    lines = replace_pronouns(lines)
    return lines

def replace_pronouns(lines):
    lines = re.sub(
        "[Ss]ie(" + SYM + ")([Ee]r)|([Ee]r)(" + SYM + ")[Ss]ie",
        "\g<2>\g<3>" + MARKER,
        lines,
        flags=re.M,
    )  # er/sie -> er
    lines = re.sub(
        "[Ii]hr(" + SYM + ")([Ii]hm)|([Ii]hm)(" + SYM + ")[Ii]hr",
        "\g<2>\g<3>" + MARKER,
        lines,
        flags=re.M,
    )  # ihr/ihm -> ihm
    lines = re.sub(
        "[Ss]ie(" + SYM + ")([Ii]hn)|([Ii]hn)(" + SYM + ")[Ss]ie",
        "\g<2>\g<3>" + MARKER,
        lines,
        flags=re.M,
    )  # sie/ihn -> ihn
    return lines

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)

    args = parser.parse_args()

    with open(args.text) as f:
        lines = f.read()

    lines = auto_deg_re(lines)

    print(lines)
