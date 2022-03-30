import argparse
import copy
import json
import logging
import os
import sys

from flair.embeddings import FlairEmbeddings
from auto_deg_re import auto_deg_re

from tokenizer import tokenizer


def auto_deg(text):
    invBI = auto_deg_re(text)
    tokenized = tokenizer(invBI)
    repl = replacements(tokenized)
    return " ".join([x for line in repl for x in line])


def find_best_replacement(word_idx, sentence, replacements):
    if len(replacements) == 1:
        sentence[word_idx] = replacements[0]
    else:
        flair_forward_embedding = FlairEmbeddings("de-forward")
        best_perplexity = 0
        best_sentence = None
        for replacement in replacements:
            sentence_copy = copy.deepcopy(sentence)
            sentence_copy[word_idx] = replacement
            perpl = flair_forward_embedding.lm.calculate_perplexity(
                " ".join(sentence_copy)
            )
            logging.debug(
                "Calculated perplexity. perplexity='%s', sentence='%s'",
                perpl,
                sentence_copy,
            )
            if best_sentence is None or best_perplexity > perpl:
                best_sentence = sentence_copy
                best_perplexity = perpl

        logging.debug(f"Best Sentence: {best_sentence}")
        sentence = best_sentence
    return sentence


def replacements(sents):
    sents_with_replacements = []
    replacements = {}
    dirname = os.path.dirname(__file__)
    if os.path.exists(dirname + "/replacements.json"):
        with open(dirname + "/replacements.json") as f:
            replacements = json.load(f)
            for sentence in sents:
                sent_with_repl = sentence
                for idx, token in enumerate(sentence):
                    if token in replacements:
                        sent_with_repl = find_best_replacement(
                            idx, sentence, replacements[token]
                        )
                        sent_with_repl.insert(idx + 1, "<GENDERLY>")
                sents_with_replacements.append(sent_with_repl)
        return sents_with_replacements

    else:
        print("Error: replacements not found!")
        sys.exit(1)

    return sents


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)

    args = parser.parse_args()

    with open(args.text) as f:
        lines = f.read()
    print("Auto degendered: ", auto_deg(lines))
