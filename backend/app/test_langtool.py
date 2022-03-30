from fastapi.testclient import TestClient

from .main import app, langtool_match_from_model

client = TestClient(app)


def test_check():
    response = client.post("/check", json={"text": "Die Lehrer singen ein Lied"})
    assert response.status_code == 200
    assert response.json() == {
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
        "matches": [
            {
                "message": "Dieser Begriff sollte gegendert werden.",
                "offset": 4,
                "length": 6,
                "replacements": [],
                "context": {"text": "Die Lehrer singe", "offset": 4, "length": 6},
            }
        ],
    }


def test_langtool_from_model():
    text = "Lorem ipsum dolor sit amet"
    match = {"offset": 10, "length": 2, "class": "Y"}
    langtool_match = langtool_match_from_model(text, match, 0)
    print(langtool_match)
    assert langtool_match["offset"] == 10
    assert langtool_match["length"] == 2
    assert langtool_match["context"]["text"] == "m "
    assert langtool_match["context"]["offset"] == 0
    assert langtool_match["context"]["length"] == 2


def test_langtool_from_model2():
    text = "Lorem ipsum dolor sit amet"
    match = {"offset": 10, "length": 2, "class": "Y"}
    langtool_match = langtool_match_from_model(text, match, 2)
    print(langtool_match)
    assert langtool_match["offset"] == 10
    assert langtool_match["length"] == 2
    assert langtool_match["context"]["text"] == "sum do"
    assert langtool_match["context"]["offset"] == 2
    assert langtool_match["context"]["length"] == 2


def test_langtool_from_model_more_context_than_possible():
    text = "Lorem"
    match = {"offset": 2, "length": 2, "class": "Y"}
    langtool_match = langtool_match_from_model(text, match, 10)
    print(langtool_match)
    assert langtool_match["offset"] == 2
    assert langtool_match["length"] == 2
    assert langtool_match["context"]["text"] == "Lorem"
    assert langtool_match["context"]["offset"] == 2
    assert langtool_match["context"]["length"] == 2


def test_langtool_from_model_more_context_in_one_direction():
    text = "Lorem"
    match = {"offset": 2, "length": 2, "class": "Y"}
    langtool_match = langtool_match_from_model(text, match, 2)
    print(langtool_match)
    assert langtool_match["offset"] == 2
    assert langtool_match["length"] == 2
    assert langtool_match["context"]["text"] == "Lorem"
    assert langtool_match["context"]["offset"] == 2
    assert langtool_match["context"]["length"] == 2
