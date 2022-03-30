from pathlib import Path

import click
from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import FlairEmbeddings, StackedEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer


@click.command()
@click.argument("CORPUS_FOLDER", type=Path)
@click.argument("MODEL_FOLDER", type=Path)
@click.option("--tag-type", default="genderly")
def main(corpus_folder, model_folder, tag_type):
    columns = {0: "text", 1: tag_type}
    corpus: Corpus = ColumnCorpus(
        corpus_folder,
        columns,
        train_file="train.txt",
        dev_file="dev.txt",
        test_file="test.txt",
    )

    tag_dictionary = corpus.make_label_dictionary(tag_type)
    print(tag_dictionary)

    embedding_types = [
        FlairEmbeddings("de-forward"),
        FlairEmbeddings("de-backward"),
    ]

    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

    tagger: SequenceTagger = SequenceTagger(
        hidden_size=256,
        embeddings=embeddings,
        tag_dictionary=tag_dictionary,
        tag_type=tag_type,
        use_crf=True,
    )

    trainer: ModelTrainer = ModelTrainer(tagger, corpus)
    trainer.train(model_folder, learning_rate=0.1, mini_batch_size=128, max_epochs=5)


if __name__ == "__main__":
    main()
