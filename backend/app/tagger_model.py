import enum
import os
import threading
from pathlib import Path

import appdirs
import requests
from flair.models import SequenceTagger
from flair.tokenization import SegtokSentenceSplitter
import config


class TagClass(enum.Enum):
    YES = "yes"
    MAYBE = "maybe"
    NO = "no"


class TaggerModel:
    def _download_model(self, url, path):
        with open(path, "wb") as f:
            req = requests.get(url, stream=True)
            for chunk in req.iter_content(chunk_size=4096):
                f.write(chunk)

    def _get_model(self):
        data_dir = Path(appdirs.user_data_dir("genderly"))
        models_dir = data_dir / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        model_path = models_dir / self.MODEL
        if not os.path.exists(model_path):
            self._download_model(self.MODEL_URL, model_path)
        return str(model_path)


class GenderizerModel(TaggerModel):
    MAYBE_PROP = 0.2
    MODEL = "model.pt"
    MODEL_URL = config.MODEL_URL
    TAG_CLASS = config.TAG_CLASS
    YES_TAG = "Y"

    def __init__(self):
        self.model = None
        self.splitter = None
        self.init_lock = threading.Lock()

    def _lazy_init(self):
        with self.init_lock:
            if self.model is None:
                self.model = SequenceTagger.load(self._get_model())
            if self.splitter is None:
                self.splitter = SegtokSentenceSplitter()

    def get_y_class(self, token):
        if token.get_tag(self.TAG_CLASS).value == self.YES_TAG:
            return TagClass.YES

        prob = self.get_y_prob(token)
        if prob >= self.MAYBE_PROP:
            return TagClass.MAYBE
        return TagClass.NO

    def get_y_prob(self, token):
        for tag in token.get_tags_proba_dist("genderizer"):
            if tag.value == self.YES_TAG:
                return tag.score

    def predict(self, text):
        self._lazy_init()

        sentences = self.splitter.split(text)

        self.model.predict(sentences, all_tag_prob=True)
        tags = []
        offset = 0
        for sentence in sentences:
            for token in sentence:
                y_class = self.get_y_class(token)
                tags.append(
                    {
                        "offset": token.start_pos + offset,
                        "length": token.end_pos - token.start_pos,
                        "class": y_class,
                    }
                )
            offset = sentence.end_pos + 1
        return tags
