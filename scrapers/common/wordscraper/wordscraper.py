import re
import sys
from pathlib import Path

import docx


def word_scrape(worddoc):
    """Returns headlines and text body of word files as continuous plaintext"""
    doc = docx.Document(worddoc)
    raw = []
    for par in doc.paragraphs:
        # Check if paragraph is a headline/title
        if par.text and par.text[-1] not in [".", ",", ";", ":"]:
            # If it is, add punctuation and append
            headline = par.text + "."
            raw.append(headline)
        else:
            # If it is not, just append
            raw.append(par.text)
    scraped = " ".join(raw)
    # Remove excess whitespace and punctuation
    scraped = re.sub(" +", " ", scraped)
    scraped = re.sub(" . ", " ", scraped)
    return scraped


if __name__ == "__main__":
    # Fetch name of wordddoc w/o file extension
    DOC_NAME = "".join(sys.argv[1].split(".")[:-1])
    # Save as .txt and attach '_scraped'
    if not Path(f"{DOC_NAME}_scraped.txt").exists():
        with open(f"{DOC_NAME}_scraped.txt", "w", encoding="utf-8") as f:
            f.write(word_scrape(sys.argv[1]))
    else:
        print("File already exists")
