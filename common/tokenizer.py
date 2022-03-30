"""The tokenizer uses the spaCy library for most of the heavy lifting"""
import re
import sys
import warnings

import spacy

NLP_SINGLETON = None


def get_nlp():
    global NLP_SINGLETON
    if NLP_SINGLETON is None:
        NLP_SINGLETON = spacy.load("de_core_news_sm", disable=["tagger", "ner"])
    return NLP_SINGLETON


def merge_regex(doc, regex):
    # Use regex to find spans we need to merge
    indices = [m.span() for m in re.finditer(regex, doc.text, flags=re.IGNORECASE)]
    # ... and merge them
    for start, end in indices:
        with doc.retokenize() as retokenizer:
            # Since our regexes don't always match up with the token boundaries, we have to use
            # alignment_mode="expand"
            # Example: doc.text="abd def", regex="d d". This would match [2:5], buf the tokens
            # would be ['abd','def']. With the default alignment_mode of "strict", this would
            # not be a span and char_span would return None
            span = doc.char_span(start, end, alignment_mode="expand")
            if span:
                retokenizer.merge(span)
            else:
                warnings.warn(
                    f"{start}-{end} is not a span (text: '{doc.text[start:end]}')",
                    RuntimeWarning,
                )


def tokenizer(corpus):
    """After tokenization, special cases are located via their character indexes and then merged"""
    # Apply to corpus
    doc = get_nlp()(corpus)

    # Use regex to find character indexes of tokens gendered with ":"
    merge_regex(doc, r"\w+:\w+")

    # Use regex to find character indexes of tokens gendered with "()"
    merge_regex(doc, r"\w+\(\w+\)")

    # Use regex to find character indexes of tokens gendered with "/"
    merge_regex(doc, r"\w+\/\w+")

    merge_regex(doc, r"<GENDERLY>")

    # Return each sentence as individual list of tokens
    tokenized = [[token.text for token in sent] for sent in doc.sents]
    return tokenized


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        contents = f.read()
        print("Raw: ", contents, "\n")
        print("Tokenized: ", tokenizer(contents), "\n")
