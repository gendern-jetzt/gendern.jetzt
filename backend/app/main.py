from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .tagger_model import GenderizerModel, TagClass

app = FastAPI()

LANGTOOL_CONTEXT_LENGTH = 5
model = GenderizerModel()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/languages")
def languages():
    return [{"name": "German", "code": "de", "longCode": "de-DE"}]


@app.get("/words")
def word():
    return []


class CheckRequest(BaseModel):
    text: str


def langtool_match_from_model(text, model_match, context_len=0):
    context_start = max(0, model_match["offset"] - context_len)
    context_length = model_match["length"] + 2 * context_len
    context_offset = model_match["offset"] - context_start

    message = ""
    if model_match["class"] == TagClass.YES:
        message = "Dieser Begriff sollte gegendert werden."
    elif model_match["class"] == TagClass.MAYBE:
        message = "Dieser Begriff sollte vermutlich gegendert werden."
    return {
        "message": message,
        "offset": model_match["offset"],
        "length": model_match["length"],
        "replacements": [],
        "context": {
            "text": text[context_start : context_start + context_length],
            "offset": context_offset,
            "length": model_match["length"],
        },
    }


@app.post("/check")
def check(req: CheckRequest):
    matches = []
    for match in model.predict(req.text):
        if match["class"] in [TagClass.YES, TagClass.MAYBE]:
            matches.append(
                langtool_match_from_model(req.text, match, LANGTOOL_CONTEXT_LENGTH)
            )

    return {
        "software": {
            "name": "genderly",
            "version": "0.1.0",
            "buildDate": "",
            "apiVersion": 1,
            "premium": True,
            "premiumHint": "",
            "status": "",
        },
        "warnings": {"incompleteResults": False},
        "language": {
            "name": "German (Germany)",
            "code": "de-DE",
            "detectedLanguage": {
                "name": "German (Germany)",
                "code": "de-DE",
                "confidence": 1,
            },
        },
        "matches": matches,
    }
