# Corpus generation pipeline

This directory contains the corpus generation pipeline for genderly.
It currently consists of a server component to store texts in a database.

## Server

You can find the server in `server/`.
To start it, you need to install [python poetry](https://python-poetry.org).
After that you can run

```shell
poetry install
```

to install all dependencies and then run

```shell
FLASK_APP=server poetry run flask run -p 8000
```

to start a local server on port 8000.

## csv edit

### export

In order to export samples from the db use the export.py script.

Example call:
```shell
poetry run python export_csv.py --max 50 --url http://url/to/genderly/corpus
```
where the --max argument determines the sentences that shall be exported.

### import

In order to import samples to the db use the import.py script.

Example call:
```shell
poetry run python import_csv.py --file [FILENAMAE].csv --url http://url/to/genderly/corpus
```
