from .tokenizer import tokenizer


def test_url():
    assert tokenizer("https://example.com/example1/example2") == [
        ["https://example.com/example1/example2"]
    ]


def test_basic():
    assert tokenizer(
        "Von der Corona-Pandemie gebeutelte Friseur:innen, VeranstalterInnen, Verkäufer*innen, "
        "Kassierer_innen, Musiker/innen und Pfleger(innen) können ein Lied davon singen: Super "
        "uncool! Hier noch ein zweiter Satz, um das Splitten von Sätzen in SpaCy zu überprüfen.",
    ) == [
        [
            "Von",
            "der",
            "Corona-Pandemie",
            "gebeutelte",
            "Friseur:innen",
            ",",
            "VeranstalterInnen",
            ",",
            "Verkäufer*innen",
            ",",
            "Kassierer_innen",
            ",",
            "Musiker/innen",
            "und",
            "Pfleger(innen)",
            "können",
            "ein",
            "Lied",
            "davon",
            "singen",
            ":",
        ],
        ["Super", "uncool", "!"],
        [
            "Hier",
            "noch",
            "ein",
            "zweiter",
            "Satz",
            ",",
            "um",
            "das",
            "Splitten",
            "von",
            "Sätzen",
            "in",
            "SpaCy",
            "zu",
            "überprüfen",
            ".",
        ],
    ]


def test_text_url_mix():
    assert tokenizer(
        "diese website fand ich lustig https://example.com/genderly/blablablub",
    ) == [
        [
            "diese",
            "website",
            "fand",
            "ich",
            "lustig",
            "https://example.com/genderly/blablablub",
        ]
    ]
