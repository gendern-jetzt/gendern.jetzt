import json
import re
import sys

import syntok.segmenter as segmenter
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from langdetect import detect_langs, lang_detect_exception

from db import db as database
from db import orm

sys.path += ["../../common"]
from auto_deg import auto_deg
from tokenizer import tokenizer

app = Flask(__name__)

CORS(app)


def is_lang(text, lang, min_prob=0.9):
    try:
        for res in detect_langs(text):
            if res.lang == lang:
                return res.prob >= min_prob
    except lang_detect_exception.LangDetectException:
        pass
    return False


def tokenize(text, source_text):
    for paragraph in segmenter.process(text):
        for sentence in paragraph:
            tokens = [x.value for x in sentence]
            joined_tokens = " ".join(tokens)
            sent = database.Sentence(
                text=source_text, sentence_gendered=joined_tokens, to_gender=True
            )
            yield sent.to_dict()


def check_text(cleaned_text):
    ad_text = auto_deg(cleaned_text)
    return is_lang(cleaned_text, lang="de", min_prob=0.9) and (
        tokenizer(ad_text) != tokenizer(cleaned_text)
    )


def check_sent(sent):
    return (
        re.search(
            r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+"
            r"|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|"
            r"[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",
            sent,
        )
        or re.search(r"\d{2}\:\d{2}", sent)
    )


def insert_text(data):
    if not data:
        abort(400)
    if (
        not isinstance(data.get("source", None), str)
        or not isinstance(data.get("source_id", None), str)
        or not isinstance(data.get("raw_data", None), str)
        or not isinstance(data.get("cleaned_text", None), str)
    ):
        abort(400)

    query = database.Text.select(
        lambda t: t.source == data.get("source")
        and t.source_id == data.get("source_id")
    )
    if query.first():
        return {"warning": "Text is already in database, skipping"}

    text = database.Text(
        source=data.get("source"),
        source_id=data.get("source_id"),
        raw_data=data.get("raw_data"),
        cleaned_text=data.get("cleaned_text"),
    )
    if not check_text(data.get("cleaned_text")):
        text.state = "REJECTED"
        return []

    sents = list(tokenize(data["cleaned_text"], text))

    return sents


@app.route("/add_text", methods=["POST"])
def add_text():
    data = request.get_json()

    with orm.db_session():
        return jsonify(insert_text(data))


@app.route("/add_texts", methods=["POST"])
def add_texts():
    data = request.get_json()
    if not isinstance(data, list):
        abort(400)

    with orm.db_session():
        return jsonify([insert_text(x) for x in data])


@app.route("/", methods=["GET"])
def list_texts():
    with orm.db_session():
        data = orm.select(t for t in database.Text if database.Text.state == "ACCEPTED")
        return jsonify([x.to_dict() for x in data[:5]])


@app.route("/list_sents", methods=["GET"])
def list_sents():
    state = request.args.get("state")
    with orm.db_session():
        if state:
            data = orm.select(s for s in database.Sentence if s.state == state)
        else:
            data = orm.select(s for s in database.Sentence)
        return jsonify([x.to_dict() for x in data[:]])


@app.route("/export", methods=["GET"])
def export_data():
    max_export = int(request.args.get("max"))
    with orm.db_session():
        data = orm.select(
            s for s in database.Sentence if s.state == "AUTO_DEG" and s.to_gender
        )
        data_filtered = [d for d in data if not check_sent(d.sentence_ungendered)]
        data_selection = data_filtered[: min(len(data), max_export)]
        for d in data_selection:
            d.state = "EXPORTED"

        return jsonify([x.to_dict() for x in data_selection])


@app.route("/import", methods=["POST"])
def import_data():
    df = json.loads(request.json)
    with orm.db_session():
        for row in df:
            database.Sentence[row["id"]].sentence_ungendered = row[
                "manually_ungendered"
            ]
            database.Sentence[row["id"]].state = "IMPORTED"
            database.Sentence[row["id"]].to_gender = False
    return ("", 200)


@app.route("/autoDeg", methods=["GET"])
def autoDeg():
    with orm.db_session():
        data = orm.select(s for s in database.Sentence if s.state == "NEW")
        lim = request.args.get("lim")
        auto_degendered = 0
        if lim is None:
            for d in data:
                try:
                    d.sentence_ungendered = auto_deg(d.sentence_gendered)
                except Exception:
                    d.state = "AUTO_DEG_FAILED"
                    continue
                if not re.search(r"\w[*:/]\w", d.sentence_ungendered):
                    d.to_gender = False
                auto_degendered += 1
                d.state = "AUTO_DEG"
        else:
            lim = int(lim)
            for d in data[:lim]:
                try:
                    d.sentence_ungendered = auto_deg(d.sentence_gendered)
                except Exception:
                    d.state = "AUTO_DEG_FAILED"
                    continue
                if not re.search(r"\w[*:/]\w", d.sentence_ungendered):
                    d.to_gender = False
                auto_degendered += 1
                d.state = "AUTO_DEG"
        return jsonify({"number of sentences autodegendered": auto_degendered})


@app.route("/export_corpus", methods=["GET"])
def export_corpus():
    with orm.db_session():
        data = orm.select(
            x.sentence_ungendered
            for x in database.Sentence
            if (x.state == "AUTO_DEG" and not x.to_gender) or (x.state == "IMPORTED")
        )
        return jsonify(list(data))
